from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .tasks import executar_sync_tesouro
from django.conf import settings

def start_scheduler():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Agenda para rodar de 1 em 1 minuto
    scheduler.add_job(
        executar_sync_tesouro,
        trigger='interval',
        minutes=1,
        id='sync_tesouro_1min',
        max_instances=1,
        replace_existing=True,
    )

    try:
        scheduler.start()
    except Exception as e:
        print(f"Erro ao iniciar scheduler: {e}")