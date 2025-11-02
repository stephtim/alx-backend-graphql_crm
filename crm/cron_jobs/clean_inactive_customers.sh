#!/bin/bash

# Absolute path to your Django project root
PROJECT_DIR="/home/username/alx-backend-graphql_crm"
LOG_FILE="/tmp/customer_cleanup_log.txt"

cd $PROJECT_DIR

# Activate virtual environment if needed
source venv/bin/activate

# Run Django shell command to delete customers inactive for 1 year
DELETED_COUNT=$(python manage.py shell -c "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta

cutoff_date = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(order__isnull=True, created_at__lt=cutoff_date).delete()
print(deleted)
")

# Log with timestamp
echo \"\$(date '+%Y-%m-%d %H:%M:%S') - Deleted \$DELETED_COUNT inactive customers.\" >> $LOG_FILE
