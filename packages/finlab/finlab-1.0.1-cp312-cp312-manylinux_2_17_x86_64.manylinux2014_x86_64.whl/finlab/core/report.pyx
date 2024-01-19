# distutils: language=c++

from collections.abc import Iterable
from pkgutil import iter_modules
import pandas as pd
import numpy as np
import importlib
import datetime
import string
import random
import base64
import socket
import time
import math
import json
import gzip
import re
import os
import finlab
from finlab import ffn_core
from finlab import get_token
from finlab.utils import logger, requests
from finlab import market_info
from finlab.utils import get_tmp_dir
import http.server
import socketserver
import threading
from pkg_resources import resource_filename
cimport numpy as np
cimport cython


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef query_data(np.ndarray df, np.ndarray[np.int64_t, ndim=1] idx_d, np.ndarray[np.int64_t, ndim=1] idx_s):
    cdef int n = len(idx_d)
    cdef list result = [None] * n
    cdef int i
    cdef np.int64_t s, d

    # Placeholder for default value depending on dtype
    cdef default_value
    
    if df.dtype == np.float64:
        default_value = np.nan
    elif df.dtype == np.int64:
        default_value = -1
    elif df.dtype == np.int8:
        default_value = -1
    elif df.dtype == np.bool_:
        default_value = False
    elif df.dtype == np.object_:  # Assuming str type
        default_value = None
    else:
        raise ValueError("Unsupported dtype")

    for i in range(n):
        s, d = idx_s[i], idx_d[i]
        result[i] = default_value if s == -1 else df[d, s]

    return result


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int64):
            return int(obj)
        return super(CustomEncoder, self).default(obj)


def is_in_vscode():
    for k in os.environ.keys():
        if 'VSCODE' in k:
            return True
    return False

daily_return = lambda s: s.resample('1d').last().dropna().pct_change()

def safe_division(n, d):
    return n / d if d else 0

calc_cagr = (
    lambda s: (s.add(1).prod()) ** safe_division(365.25, (s.index[-1] - s.index[0]).days) - 1 
    if len(s) > 1 else 0)

    
server_port = None

def find_latest_file(directory, pattern):
    candidates = [f for f in os.listdir(directory) if re.match(pattern, f)]
    if not candidates:
        raise FileNotFoundError(f"No file found matching pattern '{pattern}'")
    return max(candidates, key=lambda f: os.path.getctime(os.path.join(directory, f)))


def start_server():

    # get a random port
    port = 8000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        port = s.getsockname()[1]

    if server_port is not None:
        return

    Handler = http.server.SimpleHTTPRequestHandler

    def run_server():

        global server_port
        os.chdir(get_tmp_dir())
        with socketserver.TCPServer(("127.0.0.1", port), Handler) as httpd:
            server_port = port
            httpd.serve_forever()

    server_thread = threading.Thread(target=run_server)
    server_thread.start()


def default_serialize(obj):
    if isinstance(obj, np.int64):
        return int(obj)
    raise TypeError(
        f"Object of type '{obj.__class__.__name__}' is not JSON serializable")

def check_environment():
    env = os.environ

    if 'COLAB_GPU' in env:
        return 'Google Colab'

    if 'VSCODE_PID' in env:
        return 'VSCode'

    if 'JUPYTERHUB_SERVICE_PREFIX' in env:
        return 'Jupyter Lab'

    if 'JPY_PARENT_PID' in env:
        return 'Jupyter Notebook'

    return 'Unknown'

class Report(object):

    def __init__(self, creturn, position, fee_ratio, tax_ratio, trade_at, next_trading_date, market_info):
        # cumulative return
        self.creturn = creturn
        self.daily_creturn = self.creturn.resample('1d').last().dropna().ffill().rebase()

        # benchmark return
        self.benchmark = market_info.get_benchmark()
        if isinstance(self.benchmark, pd.Series) and self.benchmark.index.tz is not None:
            self.benchmark.index = pd.Series(self.benchmark.index).dt.tz_convert(position.index.tz)
        if len(self.benchmark) == 0:
            self.benchmark = pd.Series(1, index=self.creturn.index)

        self.daily_benchmark = self.benchmark\
            .dropna().reindex(self.daily_creturn.index, method='ffill') \
            .ffill().rebase()
        
        # position 
        self.position = position
        self.fee_ratio = fee_ratio
        self.tax_ratio = tax_ratio
        self.trade_at = trade_at
        self.update_date = position.index[-1] if len(position) > 0 else datetime.datetime.now()
        self.asset_type = 'tw_stock' if (
                position.columns.str.find('USDT') == -1).all() else 'crypto'

        position_changed = position.diff().abs().sum(axis=1)
        self.last_trading_date = position_changed[position_changed != 0].index[-1] \
            if (position_changed != 0).sum() != 0 else \
            position.index[0] if len(position) > 0 else datetime.datetime.now()

        self.next_trading_date = next_trading_date
        self.market_info = market_info
        self.weights = None
        self.next_weights = None
        self.actions = None


    def display(self, lagacy=False, save_report_path=None):
        if not lagacy:
            j = self.to_json()
            j['trades'] = json.loads(self.trades.to_json(orient='records'))
            json_str = json.dumps(j, default=default_serialize)
            position_str = json.dumps(self.position_info2(), default=default_serialize)

            # pattern = r"everything\.js-\w+\.js"
            # directory = os.path.join(get_tmp_dir(), 'dist/')
            # js_path = os.path.join(directory, find_latest_file(directory, pattern))
            js_path = resource_filename('finlab.core', 'everything.js')
            ctxt = open(js_path, encoding='utf-8').read()

            lines = ctxt.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('export'):
                    break
            ctxt = '\n'.join(lines[:i])

            http_txt = """<!DOCTYPE html>
        <html lang="en" class="bg-base-200">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/daisyui@3.7.3/dist/full.css" rel="stylesheet" type="text/css" />
            <script src="https://cdn.tailwindcss.com"></script>
            <script>
                
            </script>
            <title>Web Component Example</title>
        </head>
        <body class="bg-base-200">
            <script>const reportJson = """+json_str+"""</script>
            <script>const positionJson = """+position_str+"""</script>
            <strategy-analytic></strategy-analytic>
            <script type="module">
                """+ctxt+"""
                console.log('create report')
                console.log('reportPosition', positionJson)
                const report = new Report(reportJson.timestamps, reportJson.strategy, reportJson.benchmark, reportJson.trades, reportJson.metrics)
                console.log('create report finish', report)
                report.metrics.backtest.startDate = new Date(report.metrics.backtest.startDate)
                report.metrics.backtest.endDate = new Date(report.metrics.backtest.endDate)
                report.metrics.backtest.updateDate = new Date(report.metrics.backtest.updateDate)
                report.metrics.backtest.nextTradingDate = new Date(report.metrics.backtest.nextTradingDate)
                report.metrics.backtest.livePerformanceStart = new Date(report.metrics.backtest.livePerformanceStart)


                    function convertTrade(trade) {
                        return Object.fromEntries(
                            Object.entries(trade).map(([key, val]) => {
                            let newkey = key;
                            let newval = val;

                    switch (key) {
                        case 'bmfe':
                        break;
                        case 'entry_date':
                        newkey = 'entry';
                        newval = val ? new Date(val) : null;
                        break;
                        case 'entry_index':
                        newkey = 'entryIndex';
                        break;
                        case 'entry_sig_date':
                        newkey = 'entrySig';
                        newval = val ? new Date(val) : null;
                        break;
                        case 'exit_date':
                        newkey = 'exit';
                        newval = val ? new Date(val) : null;
                        break;
                        case 'exit_index':
                        newkey = 'exitIndex';
                        break;
                        case 'exit_sig_date':
                        newkey = 'exitSig';
                        newval = val ? new Date(val) : null;
                        break;
                        case 'gmfe':
                        break;
                        case 'mae':
                        break;
                        case 'mdd':
                        break;
                        case 'pdays':
                        break;
                        case 'period':
                        break;
                        case 'position':
                        break;
                        case 'return':
                        break;
                        case 'stock_id':
                        newkey = 'stockId';
                        break;
                        case 'trade_price@entry_date':
                        newkey = 'entryPrice';
                        break;
                        case 'trade_price@exit_date':
                        newkey = 'exitPrice';
                        break;
                    }
                    return [newkey, newval];
                    })
                );

                }

                let theme = 'dark'

                if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                    console.log('User prefers dark theme');
                } else {
                    console.log('User prefers light theme or has no preference');
                    theme = 'light'
                }
                theme = localStorage.getItem('theme') || theme

                document.documentElement.setAttribute('data-theme', theme);
                report.trades = report.trades.map(convertTrade)

                console.log(report)

                const div = document.getElementById('panel')

                const sa = new StrategyAnalytic({
                    target: div,
                    props: {
                        report: report,
                        browser: true,
                        theme: theme,
                        lang: 'zh-tw',
                        reportPosition: positionJson
                    }
                });

                document.getElementById('theme-toggler').addEventListener('change', (e) => {
                    const theme = sa.theme === 'light' ? 'dark' : 'light'
                    document.documentElement.setAttribute('data-theme', theme);
                    sa.theme = theme
                    localStorage.setItem('theme', theme)
                })

            </script>

        <div>

        <div style="background:black">

        <div class="fixed flex w-full h-screen bg-mask-left">
                <div class="bg-gradient w-full h-screen right-0"></div>
            </div>
            <div class="fixed flex w-full h-screen bg-mask-right">
                <div class="bg-gradient w-full h-screen right-0"></div>
            </div>
        </div>
        <div class="fixed top-4 right-4" style="z-index: 100">
            <label class="swap swap-rotate">
    
                <!-- this hidden checkbox controls the state -->
                <input type="checkbox" class="theme-controller" id="theme-toggler"/>
                
                <!-- sun icon -->
                <svg class="swap-on fill-current w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z"/></svg>
                
                <!-- moon icon -->
                <svg class="swap-off fill-current w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z"/></svg>
                
            </label>
        </div>

        </div>
        <div id="panel" style="z-index: 2;position:relative;max-width:960px" class="p-4 mx-auto rounded-2xl bg-base-200"></div>
        </body>

        <style>
* {
  border-color: #77777777 !important;
}

/* Light Theme */
[data-theme='light'] .bg-primary {
    background-color: #725bf5 !important;
}

[data-theme='light'] .bg-secondary {
    background-color: #f16365 !important;
}

[data-theme='light'] .bg-accent {
    background-color: #1dcdbc !important;
}

[data-theme='light'] .text-primary-content {
    color: white !important;
}

[data-theme='light'] .bg-base-100 {
    background-color: #E8E8E8 !important;
}

[data-theme='light'] .bg-base-200 {
    background-color: #F8F8F8 !important;
}

[data-theme='light'] .bg-base-300 {
    background-color: white !important;
}

[data-theme='light'] .text-base-content {
    color: black !important;
}

[data-theme='light'] .text-base-content-300 {
    color: #4b5563 !important; /* gray-700 */
}

[data-theme='light'] .text-base-content-200 {
    color: #6b7280 !important; /* gray-600 */
}

[data-theme='light'] .text-base-content-100 {
    color: #9ca3af !important; /* gray-500 */
}

/* Dark Theme */

[data-theme='dark'] .bg-primary {
    background-color: #7a64f5 !important;
}

[data-theme='dark'] .bg-secondary {
    background-color: #f16365 !important;
}

[data-theme='dark'] .bg-accent {
    background-color: #1dcdbc !important;
}

[data-theme='dark'] .text-primary-content {
    color: white !important;
}

[data-theme='dark'] .bg-base-100 {
    background-color: #080808 !important;
}

[data-theme='dark'] .bg-base-200 {
    background-color: #131313 !important;
}

[data-theme='dark'] .bg-base-300 {
    background-color: #242424 !important;
}

[data-theme='dark'] .text-base-content {
    color: white !important;
}

[data-theme='dark'] .text-base-content-300 {
    color: #d1d5db !important; /* gray-300 */
}

[data-theme='dark'] .text-base-content-200 {
    color: #9ca3af !important; /* gray-400 */
}

[data-theme='dark'] .text-base-content-100 {
    color: #6b7280 !important; /* gray-500 */
}

#panel {
    font-family: ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
}

        .gradient-color {
            background-clip: text;
            color: transparent;
            background-image: linear-gradient(to right, #6ef0bc, #7f22d2, #3bc0c3);
        }

        .bg-gradient {
            background-image: linear-gradient(to top, #f687b3, #7f22d2, #3bc0c3);
        }

        .bg-mask-left, .bg-mask-right {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            -webkit-mask-image: radial-gradient(circle at var(--position),
                rgba(0, 0, 0, 0.1) 0%,
                transparent 30%,
                transparent 100%);
        }

        .bg-mask-left {
            --position: left;
        }

        .bg-mask-right {
            --position: right;
        }

        .main-content {
            z-index: 2;
            position: relative;
        }

        .grid-cols-14.svelte-13tqbdu{grid-template-columns:repeat(14, minmax(0, 1fr))}
        </style>
        </html>"""

            file_path = os.path.join(get_tmp_dir(), 'report.html')

            f = open(file_path, 'w', encoding='utf-8')
            f.write(http_txt)
            f.close()

            if save_report_path is not None:
                f = open(save_report_path, 'w', encoding='utf-8')
                f.write(http_txt)
                f.close()

            from IPython.display import display, HTML
            iframe_id = 'iframe_' +''.join(random.choice(string.ascii_letters) for _ in range(10))
            iframe_code = """
                <iframe id="IFRAME" src="YOUR_URL_HERE" style="height: 600px;width: 100%;max-width:960px; border: none;border-radius:20px"></iframe>
                <script>
                    // set iframe_id into local storage
                    localStorage.setItem('iframe_id', 'IFRAME');
                    localStorage.setItem('tab', 'reset');
                    window.addEventListener('message', function (event) {
                        console.log('tab event', event)
                        const data = event.data;

                        // not message event
                        if (!data.frameHeight || !data.tab) {
                            return;
                        }

                        // not change tab
                        const prevTab = localStorage.getItem('tab');

                        console.log('prevTab', prevTab)
                        console.log('data.tab', data.tab)

                        if (prevTab === data.tab) {
                            return;
                        }

                        const iframe_id = localStorage.getItem('iframe_id');
                        console.log('iframe_id', iframe_id)
                        const iframe = document.querySelector('#'+iframe_id);

                        iframe.style.height = (data.frameHeight + 1) + 'px';
                        iframe.setAttribute('scrolling', 'no');

                        localStorage.setItem('tab', data.tab);
                    });
                </script>
            """.replace('IFRAME', iframe_id)


            environment = check_environment()

            if environment != 'Google Colab':
                start_server()

                global server_port
                check_port = 0
                while server_port is None:
                    time.sleep(0.1)
                    check_port += 1
                    if check_port > 100:
                        raise Exception('Cannot start server')

                url = f'http://localhost:{server_port}/report.html'

                display(HTML(iframe_code.replace("YOUR_URL_HERE",
                        url)))
            else:
                # cancel cell scrolling
                try:
                    from google.colab import output
                    output.no_vertical_scroll()
                except:
                    logger.warning('Cannot cancel cell scrolling')

                try:
                    import IPython
                    IPython.display.display(IPython.display.HTML(filename=file_path))
                except:
                    logger.warning('Cannot display HTML. Please install IPython to show the complete backtest results.')
        else:
            if save_report_path is not None:
                logger.warning('save_report_path is not supported in lagacy mode.')

            if self.benchmark is not None:
                performance = pd.DataFrame({
                    'strategy': self.daily_creturn,
                    'benchmark': self.daily_benchmark.reindex(self.daily_creturn.index, method='ffill')}).dropna().rebase()
            else:
                performance = pd.DataFrame({
                    'strategy': self.creturn}).dropna().rebase()

            fig = self.create_performance_figure(
                performance, (self.position != 0).sum(axis=1))

            stats = self.get_stats()
            sharpe = stats['daily_sharpe'] if stats['daily_sharpe'] == stats['daily_sharpe'] else stats['monthly_sharpe']
            imp_stats = pd.Series({
            'annualized_rate_of_return':str(round(stats['cagr']*100, 2))+'%',
            'sharpe': str(round(sharpe, 2)),
            'max_drawdown':str(round(stats['max_drawdown']*100, 2))+'%',
            'win_ratio':str(round(stats['win_ratio']*100, 2))+'%',
            }).to_frame().T
            imp_stats.index = ['']

            yearly_return_fig = self.create_yearly_return_figure(stats['return_table'])
            monthly_return_fig = self.create_monthly_return_figure(stats['return_table'])

            from IPython.display import display

            display(imp_stats)
            display(fig)
            display(yearly_return_fig)
            display(monthly_return_fig)

            if hasattr(self, 'current_trades'):
                display(self.current_trades)
            else:
                print('current position')
                if len(self.position) > 0:
                    p = self.position.iloc[-1]
                    display(p[p != 0])

    @staticmethod
    def create_performance_figure(performance_detail, nstocks):

        from plotly.subplots import make_subplots
        import plotly.graph_objs as go
        # plot performance

        def diff(s, period):
            return (s / s.shift(period) - 1)

        drawdowns = performance_detail.to_drawdown_series()

        fig = go.Figure(make_subplots(
            rows=4, cols=1, shared_xaxes=True, row_heights=[2, 1, 1, 1]))
        fig.add_scatter(x=performance_detail.index, y=performance_detail.strategy / 100 - 1,
                        name='strategy', row=1, col=1, legendgroup='performance', fill='tozeroy')
        fig.add_scatter(x=drawdowns.index, y=drawdowns.strategy, name='strategy - drawdown',
                        row=2, col=1, legendgroup='drawdown', fill='tozeroy')
        fig.add_scatter(x=performance_detail.index, y=diff(performance_detail.strategy, 20),
                        fill='tozeroy', name='strategy - month rolling return',
                        row=3, col=1, legendgroup='rolling performance', )

        if 'benchmark' in performance_detail.columns:
            fig.add_scatter(x=performance_detail.index, y=performance_detail.benchmark / 100 - 1,
                            name='benchmark', row=1, col=1, legendgroup='performance', line={'color': 'gray'})
            fig.add_scatter(x=drawdowns.index, y=drawdowns.benchmark, name='benchmark - drawdown',
                            row=2, col=1, legendgroup='drawdown', line={'color': 'gray'})
            fig.add_scatter(x=performance_detail.index, y=diff(performance_detail.benchmark, 20),
                            fill='tozeroy', name='benchmark - month rolling return',
                            row=3, col=1, legendgroup='rolling performance', line={'color': 'rgba(0,0,0,0.2)'})

        fig.add_scatter(x=nstocks.index, y=nstocks, row=4,
                        col=1, name='nstocks', fill='tozeroy')
        fig.update_layout(legend={'bgcolor': 'rgba(0,0,0,0)'},
                          margin=dict(l=60, r=20, t=40, b=20),
                          height=600,
                          width=800,
                          xaxis4=dict(
                              rangeselector=dict(
                                  buttons=list([
                                      dict(count=1,
                                           label="1m",
                                           step="month",
                                           stepmode="backward"),
                                      dict(count=6,
                                           label="6m",
                                           step="month",
                                           stepmode="backward"),
                                      dict(count=1,
                                           label="YTD",
                                           step="year",
                                           stepmode="todate"),
                                      dict(count=1,
                                           label="1y",
                                           step="year",
                                           stepmode="backward"),
                                      dict(step="all")
                                  ]),
                                  x=0,
                                  y=1,
                              ),
                              rangeslider={'visible': True, 'thickness': 0.1},
                              type="date",
                          ),
                          yaxis={'tickformat': ',.0%', },
                          yaxis2={'tickformat': ',.0%', },
                          yaxis3={'tickformat': ',.0%', },
                          )
        return fig


    @staticmethod
    def create_yearly_return_figure(return_table):
        import plotly.express as px
        yearly_return = [round(v['YTD']*1000)/10 for v in return_table.values()]
        fig = px.imshow([yearly_return],
                        labels=dict(color="return(%)"),
                        x=list([str(k) for k in return_table.keys()]),
                        text_auto=True,
                        color_continuous_scale='RdBu_r',
                        )

        fig.update_traces(
            hovertemplate="<br>".join([
                "year: %{x}",
                "return: %{z}%",
            ])
        )

        fig.update_layout(
            height = 120,
            width= 800,
            margin=dict(l=20, r=270, t=40, b=40),
            yaxis={
                'visible': False,
            },
            title={
                'text': 'yearly return',
                'x': 0.025,
                'yanchor': 'top',
            },
            coloraxis_showscale=False,
            coloraxis={'cmid':0}
            )

        return fig

    @staticmethod
    def create_monthly_return_figure(return_table):

        if len(return_table) == 0:
            return None

        import plotly.express as px
        monthly_table = pd.DataFrame(return_table).T
        monthly_table = round(monthly_table*100,1).drop(columns='YTD')

        fig = px.imshow(monthly_table.values,
                        labels=dict(x="month", y='year', color="return(%)"),
                        x=monthly_table.columns.astype(str),
                        y=monthly_table.index.astype(str),
                        text_auto=True,
                        color_continuous_scale='RdBu_r',

                        )

        fig.update_traces(
            hovertemplate="<br>".join([
                "year: %{y}",
                "month: %{x}",
                "return: %{z}%",
            ])
        )

        fig.update_layout(
            height = 550,
            width= 800,
            margin=dict(l=20, r=270, t=40, b=40),
            title={
                'text': 'monthly return',
                'x': 0.025,
                'yanchor': 'top',
            },
            yaxis={
                'side': "right",
            },
            coloraxis_showscale=False,
            coloraxis={'cmid':0}
        )

        return fig

    def to_json(self):

        # Convert DataFrame to JSON
        json_str = self.trades.to_json(orient='records')

        # Encode JSON string into bytes
        json_bytes = json_str.encode('utf-8')

        # Compress JSON bytes with gzip
        gzip_bytes = gzip.compress(json_bytes)

        # Convert gzip bytes to base64 encoded string for easier storage and transmission
        gzip_b64_str = base64.b64encode(gzip_bytes).decode('utf-8')

        ret = {
            'timestamps': self.daily_creturn.index.astype(str).to_list(),
            'strategy': self.daily_creturn.values.tolist(),
            'benchmark': self.daily_benchmark.values.tolist(),
            'metrics': self.get_metrics(),
            'trades': gzip_b64_str
        }

        return ret

    def _to_json046(self):

        # Convert DataFrame to JSON
        json_str = self.trades.tail(500).to_json(orient='records')

        # Encode JSON string into bytes
        json_bytes = json_str.encode('utf-8')

        # Compress JSON bytes with gzip
        gzip_bytes = gzip.compress(json_bytes)

        # Convert gzip bytes to base64 encoded string for easier storage and transmission
        gzip_b64_str = base64.b64encode(gzip_bytes).decode('utf-8')

        ret = {
            'metrics': self.get_metrics(),
            'trades': gzip_b64_str
        }

        return ret


    def upload(self, name=None, mae_mfe_charts=False, display=True):

        name = os.environ.get(
            'FINLAB_FORCED_STRATEGY_NAME', None) or name or '未命名'

        head_is_eng = len(re.findall(
            r'[\u0041-\u005a|\u0061-\u007a]', name[0])) > 0
        has_cn = len(re.findall('[\u4e00-\u9fa5]', name[1:])) > 0
        if head_is_eng and has_cn:
            raise Exception('Strategy Name Error: 名稱如包含中文，需以中文當開頭。')
        for c in '()[]+-|!@#$~%^={}&*':
            name = name.replace(c, '_')

        # stats
        stats = self.get_stats()

        # creturn
        creturn = {'time': self.daily_creturn.index.astype(str).to_list(),
                   'value': self.daily_creturn.values.tolist()}

        # ndays return
        ndays_return = {d: self.get_ndays_return(
            self.daily_creturn, d) for d in [1, 5, 10, 20, 60]}
        ndays_return_benchmark = {d: self.get_ndays_return(
            self.daily_benchmark, d) for d in [1, 5, 10, 20, 60]}

        d = {
            # backtest info
            'drawdown_details': stats['drawdown_details'],
            'stats': stats,
            'returns': creturn,
            'benchmark': self.daily_benchmark.values.tolist(),
            'ndays_return': ndays_return,
            'ndays_return_benchmark': ndays_return_benchmark,
            'return_table': stats['return_table'],
            'fee_ratio': self.fee_ratio,
            'tax_ratio': self.tax_ratio,
            'trade_at': self.trade_at if isinstance(self.trade_at, str) else 'open',
            'timestamp_name': self.market_info.get_name(),
            'freq': self.market_info.get_freq(),

            # dates
            'update_date': self.update_date.isoformat(),
            'next_trading_date': self.next_trading_date.isoformat(),

            # key data
            'position': self.position_info(),
            'position2': self.position_info2(),

            # live performance
            'live_performance_start': self.live_performance_start.isoformat() if self.live_performance_start else None,
            'stop_loss': self.stop_loss,
            'take_profit': self.take_profit,
            **self._to_json046()
        }

        # import numpy as np

        # def find_ndarray_keys(d, parent_keys=[]):
        #     ndarray_keys = []
        #     for key, value in d.items():
        #         new_keys = parent_keys + [key]
        #         if isinstance(value, np.ndarray):
        #             ndarray_keys.append('.'.join(new_keys))
        #         elif isinstance(value, dict):
        #             ndarray_keys.extend(find_ndarray_keys(value, new_keys))
        #     return ndarray_keys

        
        # ndarray_keys = find_ndarray_keys(d)
        # print('ndarray_keys')
        # print(ndarray_keys)

        def upload():

            payload = {'data': json.dumps(d, cls=CustomEncoder),
                    'api_token': get_token(),
                    'collection': 'strategies',
                    'document_id': name}

            result = requests.post(
                'https://asia-east2-fdata-299302.cloudfunctions.net/write_database', data=payload).text

            # python is in website backtest
            if 'FINLAB_FORCED_STRATEGY_NAME' in os.environ:
                return {'status': 'success'}

            # create iframe
            try:
                result = json.loads(result)
            except:
                return {'status': 'error', 'message': 'cannot parse json object'}

            if 'status' in result and result['status'] == 'error':
                print('Fail to upload result to server')
                print('error message', result['message'])
                return {'status': 'error', 'message': result['status']}

            if not display:
                return {'status': 'success'}

        try:
            self.display()
            
        except Exception as e:
            print(e)
            print('Install ipython to show the complete backtest results.')
        upload()

    
    def position_info2(self):

        if not hasattr(self, 'current_trades'):
            return {
                "positions": [],
                "positionConfig": {
                    "isDailyStrategy": 1,
                    "sl": self.stop_loss,
                    "tp": self.take_profit,
                    "ts": self.trail_stop,
                    "resample": self.resample,
                    "entryTradePrice": self.trade_at,
                    "exitTradePrice": self.trade_at,
                    "scheduled": datetime.datetime.now().isoformat(),
                    "dataFreq": self.market_info.get_freq(),
                    "created": datetime.datetime.now().isoformat(),
                    "lastTimestamp": datetime.datetime.now().isoformat(),
                }
            }
        actions = []

        for idx, row in self.current_trades.iterrows():
            is_entry = row['entry_sig_date'] == self.creturn.index[-1]
            is_future_entry = row['entry_sig_date'] > self.creturn.index[-1]

            # exit today or before today
            is_exit = row['exit_sig_date'] == self.creturn.index[-1]
            is_past_exit = row['exit_sig_date'] < self.creturn.index[-1]

            # exit in futures (hold)
            is_hold = (row['exit_sig_date'] > self.creturn.index[-1]) | (row['exit_sig_date'] != row['exit_sig_date'])

            type_ = 'hold'

            if is_entry:
                type_ = 'entry'
            elif is_future_entry:
                type_ = 'entry_f'
            elif is_exit:
                type_ = 'exit'
            elif is_past_exit:
                type_ = 'exit_p'
            elif is_hold:
                type_ = 'hold'
            else:
                print(f'There is a strange type for stock {idx} {row}')
            
            if type_ == 'exit' or type_ == 'exit_p':
                reason = self.actions.loc[idx] if idx in self.actions.index else '_'
            else:
                reason = '_'

            date = row['exit_sig_date']
            if date != date:
                date = row['entry_sig_date']
            profit = row['return']
            if profit != profit:
                profit = 0
            actions.append({
                'type': type_,
                'reason': reason,
                'date': date.isoformat(),
                'profit': profit
            })

        adj_close = self.market_info.get_price('close', adj=True)
        close = self.market_info.get_price('close', adj=False)
        cmin = adj_close.iloc[-20:].min()
        cmax = adj_close.iloc[-20:].max()
        rsv20 = (adj_close.iloc[-1] - cmin) / (cmax - cmin)

        to_date_string = lambda d: d.isoformat() if d == d else None

        trades = self.current_trades.copy()
        positions = pd.DataFrame({
            'assetName': trades.index.str.split(' ').str[1],
            'assetId':trades.index.str.split(' ').str[0],
            'entryDate':trades['entry_date'].apply(to_date_string),
            'entrySigDate':trades['entry_sig_date'].apply(to_date_string),
            'exitDate':trades['exit_date'].apply(to_date_string),
            'exitSigDate':trades['exit_sig_date'].apply(to_date_string),
            'entryPrice':trades['trade_price@entry_date'],
            'exitPrice':trades['trade_price@exit_date'],
            'currentPrice':trades.index.str.split(' ').str[0].map(close.iloc[-1]),
            'profit':trades['return'],
            'currentWeight':trades['weight'],
            'nextWeight':trades['next_weights'],
            'rsv20': trades.index.str.split(' ').str[0].map(rsv20),
            'action': actions,
        }).to_dict(orient='records')

        position_config = {
            # isDailyStrategy: False,
            "isDailyStrategy": 1 if ((self.position.index.hour == 0) & (self.position.index.minute == 0) & (self.position.index.second == 0)).all() else 0,
            "sl": self.stop_loss,
            "tp": self.take_profit,
            "resample": self.resample,
            "entryTradePrice": self.trade_at,
            "exitTradePrice": self.trade_at,
            "scheduled": self.next_trading_date.isoformat(),
            "dataFreq": self.market_info.get_freq(),
            "created": datetime.datetime.now().isoformat(),
            "lastTimestamp": self.creturn.index[-1].isoformat() if len(self.creturn) > 0 else None,
        }

        return {
            "positions": positions,
            "positionConfig": position_config,
        }

    def position_info(self):

        if not hasattr(self, 'current_trades'):
            return pd.DataFrame(columns=['status', 'weight', 'next_weight', 
                                'entry_date', 'exit_date', 'return', 'entry_price'])\
                                .to_dict('index')
        
        current_trades = self.current_trades

        default_status = pd.Series('hold', index=current_trades.index)
        default_status.loc[current_trades.exit_sig_date.notna()] = 'exit'
        if self.resample == None:
            default_status[current_trades.exit_sig_date.isnull()] = 'hold'
            default_status[current_trades.exit_sig_date.notna()] = 'exit'

        trade_at = self.trade_at if isinstance(self.trade_at, str) else 'close'

        trade_at_zh = {
                'close': '收盤',
                'open': '開盤',
                'open|close': '盤中',
                }

        status = self.actions.reindex(current_trades.index).fillna(default_status)

        ret = pd.DataFrame({
            'status': status,
            'weight': current_trades.weight,
            'next_weight': current_trades.next_weights,
            'entry_date': current_trades.entry_sig_date.apply(lambda d: d.isoformat() if d else ''),
            'exit_date': current_trades.exit_sig_date.apply(lambda d: d.isoformat() if d else ''),
            'return': current_trades['return'].fillna(0),
            'entry_price': current_trades['trade_price@entry_date'].fillna(0),
        }, index=current_trades.index)

        ret['latest_sig_date'] = pd.DataFrame({'entry': ret.entry_date, 'exit': ret.exit_date}).max(axis=1)
        ret = ret.sort_values('latest_sig_date').groupby(level=0).last()
        ret = ret.drop(columns='latest_sig_date')

        ret = ret.to_dict('index')

        ret['update_date'] = self.update_date.isoformat()
        ret['next_trading_date'] = self.next_trading_date.isoformat()
        ret['trade_at'] = trade_at
        ret['freq'] = self.market_info.get_freq()
        ret['market'] = self.market_info.get_name()
        ret['stop_loss'] = self.stop_loss
        ret['take_profit'] = self.take_profit

        return ret

    @staticmethod
    def get_ndays_return(creturn, n):
        last_date_eq = creturn.iloc[-1]
        ref_date_eq = creturn.iloc[max(-1 - n, -len(creturn))]
        return last_date_eq / ref_date_eq - 1

    def add_trade_info(self, name, df, date_col='entry_sig_date'):

        if isinstance(date_col, str):
            date_col = [date_col]

        combined_dates = set().union(*[set(self.trades[d]) for d in date_col])
        df_temp = df.reindex(df.index.union(combined_dates), method='ffill')

        for date_name in date_col:
            dates = self.trades[date_name]
            stocks = self.trades['stock_id'].str.split(' ').str[0]

            idx_d = df_temp.index.get_indexer_for(dates)
            idx_s = df_temp.columns.get_indexer_for(stocks)

            # self.trades[f"{name}@{date_name}"] = [
            #     np.nan if s == -1 else df_temp.iloc[d, s]
            #     for s, d in zip(idx_s, idx_d)]

            self.trades[f"{name}@{date_name}"] = query_data(df_temp.values, idx_d, idx_s)


    def remove_trade_info(self, name):
        cs = [c for c in self.columns if c != name]
        self.trades = self.trades[cs]

    def get_mae_mfe(self):
        return self.mae_mfe

    def get_trades(self):
        return self.trades

    def get_stats(self, resample='1d', riskfree_rate=0.02):

        stats = self.daily_creturn.calc_stats()
        stats.set_riskfree_rate(riskfree_rate)

        # calculate win ratio
        ret = stats.stats.to_dict()
        ret['start'] = ret['start'].strftime('%Y-%m-%d')
        ret['end'] = ret['end'].strftime('%Y-%m-%d')
        ret['version'] = finlab.__version__

        trades = self.trades.dropna()
        ret['win_ratio'] = sum(trades['return'] > 0) / len(trades) if len(trades) != 0 else 0
        ret['return_table'] = stats.return_table.transpose().to_dict()
        # ret['mae_mfe'] = self.run_analysis("MaeMfe", display=False)
        # ret['liquidity'] = self.run_analysis("Liquidity", display=False)
        # ret['period_stats'] = self.run_analysis("PeriodStats", display=False)
        # ret['alpha_beta'] = self.run_analysis("AlphaBeta", display=False)

        # todo old remove
        drawdown = self.run_analysis("Drawdown", display=False)
        ret['drawdown_details'] = drawdown['strategy']['largest_drawdown']
        return ret

    def get_metrics(self, stats_=None, riskfree_rate=0.02):

        if stats_ == None:
            simple_stats = self.creturn.resample('1d').last().dropna().calc_stats()
            simple_stats.set_riskfree_rate(0.02)
            stats_ = simple_stats.stats.to_dict()


        mv = self.market_info.get_market_value()
        if len(mv) != 0:
            self.add_trade_info('market_value', mv, ['entry_date'])

        strategy_daily_return = daily_return(self.creturn)
        benchmark_daily_return = daily_return(self.benchmark).reindex(strategy_daily_return.index).fillna(0)

        from finlab.analysis.alphaBetaAnalysis import AlphaBetaAnalysis
        alpha, beta = AlphaBetaAnalysis.calculate_alpha_beta(strategy_daily_return, benchmark_daily_return)
        position_nstocks = (self.position!=0).sum(axis=1)
        monthly_return = (strategy_daily_return+1).resample('M').prod().subtract(1)
        var = monthly_return.quantile(0.05)
        cvar = monthly_return[monthly_return < var].mean()
        
        tail_right = strategy_daily_return.quantile(0.95)
        tail_left = strategy_daily_return.quantile(0.05)
        tail_ratio = abs(tail_right / tail_left) if tail_left != 0 else 1

        safe_div = lambda a, b: a / b if b != 0 else 0
        calc_profit_factor = lambda s: abs(safe_div(s[s > 0].sum(), s[s < 0].sum()))
        liquidity = self.run_analysis('liquidity', display=False)


        def calc_capacity(trades, percentage_of_volume=0.05):

            if 'turnover@entry_date' not in trades.columns:
                return 0

            accepted_money_flow = (self.trades['turnover@entry_date'] * percentage_of_volume / self.trades.position + \
                    self.trades['turnover@exit_date'] * percentage_of_volume / self.trades.position) / 2

            return accepted_money_flow.quantile(0.1)

        pos_nstocks = position_nstocks.mean()
        return {

            "backtest": {
                "startDate": self.creturn.index[0].to_pydatetime().timestamp(),
                "endDate": self.creturn.index[-1].to_pydatetime().timestamp(),
                "version": finlab.__version__,
                'feeRatio': self.fee_ratio,
                'taxRatio': self.tax_ratio,
                'tradeAt': self.trade_at if isinstance(self.trade_at, str) else 'open',
                'market': self.market_info.get_name(),
                'freq': self.market_info.get_freq(),

                # dates
                'updateDate': self.update_date.timestamp(),
                'nextTradingDate': self.next_trading_date.timestamp(),

                # live performance
                'livePerformanceStart': self.live_performance_start.timestamp() if self.live_performance_start else None,
                'stopLoss': self.stop_loss,
                'takeProfit': self.take_profit,
                'trailStop': self.trail_stop,
            },

            "profitability": {
                "annualReturn": stats_["cagr"],
                "alpha": alpha,
                "beta": beta,
                "avgNStock": pos_nstocks,
                "maxNStock": position_nstocks.max() if isinstance(position_nstocks, pd.Series) else pos_nstocks,
            },

            "risk": {
                "maxDrawdown": stats_["max_drawdown"],
                "avgDrawdown": stats_["avg_drawdown"],
                "avgDrawdownDays": stats_["avg_drawdown_days"],
                "valueAtRisk": var,
                "cvalueAtRisk": cvar
            },

            "ratio": {
                "sharpeRatio": stats_["daily_sharpe"],
                "sortinoRatio": stats_["daily_sortino"],
                "calmarRatio": stats_["calmar"],
                "volatility": stats_["daily_vol"],
                "profitFactor": calc_profit_factor(self.trades['return']) if len(self.trades) != 0 else 1,
                "tailRatio": tail_ratio,
            },

            "winrate": {
                "winRate": sum(self.trades['return'] > 0) / len(self.trades) if len(self.trades) != 0 else 0,
                "m12WinRate": stats_["twelve_month_win_perc"],
                "expectancy": self.trades['return'].mean() if len(self.trades) != 0 else 0,
                "mae": self.trades['mae'].mean() if len(self.trades) != 0 else 0,
                "mfe": self.trades['gmfe'].mean() if len(self.trades) != 0 else 0,
            },

            "liquidity": {
                "capacity": calc_capacity(self.trades, percentage_of_volume=0.05),
                "disposalStockRatio": max(liquidity['處置股']['exit'], liquidity['處置股']['entry']) if '處置股' in liquidity else 0,
                "warningStockRatio": max(liquidity['警示股']['entry'],liquidity['警示股']['exit']) if '警示股' in liquidity else 0,
                "fullDeliveryStockRatio": max(liquidity['全額交割股']['entry'], liquidity['全額交割股']['exit']) if '全額交割股' in liquidity else 0,
                "buyHigh": max(liquidity['buy_high']['entry'],liquidity['buy_high']['exit'])  if 'buy_high' in liquidity else 0,
                "sellLow": max(liquidity['sell_low']['entry'],liquidity['sell_low']['exit']) if 'sell_low' in liquidity else 0,
            }
        }



    def run_analysis(self, analysis, display=True, **kwargs):

        # get the instance of analysis
        if isinstance(analysis, str):

            if analysis[-8:] != 'Analysis':
                analysis += 'Analysis'

            # get module
            module_name = 'finlab.analysis.' + analysis[0].lower() + analysis[1:]

            if importlib.util.find_spec(module_name) is None:
                import finlab.analysis as module
                submodules = []
                for submodule in iter_modules(module.__path__):
                    if '_' not in submodule.name:
                        submodules.append(submodule.name[:-8:])

                error = f"Cannot find {module_name}. Possible candidates are " + str(submodules)[1:-1]
                raise Exception(error)

            analysis_module = importlib.import_module(module_name)

            # create an instance from module
            analysis_class = analysis[0].upper() + analysis[1:]

            analysis = getattr(analysis_module, analysis_class)(**kwargs)

        # calculate additional trade info for analysis
        additional_trade_info = analysis.calculate_trade_info(self)
        for v in additional_trade_info:
            self.add_trade_info(*v)

        # analysis and return figure or data as result
        result = analysis.analyze(self)

        if display:
            return analysis.display()

        return result

    def display_mae_mfe_analysis(self, **kwargs):
        return self.run_analysis("MaeMfeAnalysis", **kwargs)
