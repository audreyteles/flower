import os

from tornado.web import StaticFileHandler, url

from .api import control, tasks, workers
from .utils import gen_cookie_secret
from .views import auth, monitor
from .views.broker import BrokerView
from .views.error import NotFoundErrorHandler
from .views.tasks import TasksDataTable, TasksView, TaskView
from .views.workers import WorkersView, WorkerView

# nginx base_path
basepath = '/flower'

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    cookie_secret=gen_cookie_secret(),
    static_url_prefix=f'{basepath}/static/',
    login_url=(f'{basepath}/login',
)


handlers = [
    # App
    url(f"{basepath}/", WorkersView, name='main'),
    url(f"{basepath}/workers", WorkersView, name='workers'),
    url(f"{basepath}/worker/(.+)", WorkerView, name='worker'),
    url(f"{basepath}/task/(.+)", TaskView, name='task'),
    url(f"{basepath}/tasks", TasksView, name='tasks'),
    url(f"{basepath}/tasks/datatable", TasksDataTable),
    url(f"{basepath}/broker", BrokerView, name='broker'),
    
    # Worker API
    (f"{basepath}/api/workers", workers.ListWorkers),
    (f"{basepath}/api/worker/shutdown/(.+)", control.WorkerShutDown),
    (f"{basepath}/api/worker/pool/restart/(.+)", control.WorkerPoolRestart),
    (f"{basepath}/api/worker/pool/grow/(.+)", control.WorkerPoolGrow),
    (f"{basepath}/api/worker/pool/shrink/(.+)", control.WorkerPoolShrink),
    (f"{basepath}/api/worker/pool/autoscale/(.+)", control.WorkerPoolAutoscale),
    (f"{basepath}/api/worker/queue/add-consumer/(.+)", control.WorkerQueueAddConsumer),
    (f"{basepath}/api/worker/queue/cancel-consumer/(.+)", control.WorkerQueueCancelConsumer),
    
    # Task API
    (f"{basepath}/api/tasks", tasks.ListTasks),
    (f"{basepath}/api/task/types", tasks.ListTaskTypes),
    (f"{basepath}/api/queues/length", tasks.GetQueueLengths),
    (f"{basepath}/api/task/info/(.*)", tasks.TaskInfo),
    (f"{basepath}/api/task/apply/(.+)", tasks.TaskApply),
    (f"{basepath}/api/task/async-apply/(.+)", tasks.TaskAsyncApply),
    (f"{basepath}/api/task/send-task/(.+)", tasks.TaskSend),
    (f"{basepath}/api/task/result/(.+)", tasks.TaskResult),
    (f"{basepath}/api/task/abort/(.+)", tasks.TaskAbort),
    (f"{basepath}/api/task/timeout/(.+)", control.TaskTimout),
    (f"{basepath}/api/task/rate-limit/(.+)", control.TaskRateLimit),
    (f"{basepath}/api/task/revoke/(.+)", control.TaskRevoke),
    
    # Metrics
    (f"{basepath}/metrics", monitor.Metrics),
    (f"{basepath}/healthcheck", monitor.Healthcheck),
    
    # Static
    (f"{basepath}/static/(.*)", StaticFileHandler, {"path": settings['static_path']}),
    
    # Auth
    (f"{basepath}/login", auth.LoginHandler),

    # Error
    (r".*", NotFoundErrorHandler),
]

]
