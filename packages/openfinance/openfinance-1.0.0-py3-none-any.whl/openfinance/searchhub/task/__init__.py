from openfinance.searchhub.task.analysis.analysis_task import AnalysisTask
from openfinance.searchhub.task.search.search_task import SearchTask
from openfinance.searchhub.task.compare.compare_task import CompareTask
from openfinance.searchhub.task.role.role_task import RoleTask
from openfinance.searchhub.task.search_sql.search_sql_task import SearchSqlTask
from openfinance.searchhub.task.percept.percept_task import PerceptTask
from openfinance.searchhub.task.percept.online_percept_task import OnlinePerceptTask


candidate_tasks = [
    AnalysisTask,
    SearchTask,
    CompareTask,
    RoleTask,
    SearchSqlTask,
    PerceptTask,
    OnlinePerceptTask
]