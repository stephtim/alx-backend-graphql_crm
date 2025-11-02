#!/bin/bash
# clean_inactive_customers.sh
# Deletes customers with no orders in the past year and logs result

# Navigate to the Django project root
cd "$(dirname "$0")/../.." || exit

# Run the Django shell command to delete inactive customers
count=$(python3 manage.py shell <<EOF
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

cutoff_date = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(order__isnull=True, created_at__lt=cutoff_date).delete()
print(deleted)
EOF
)

# Log output with timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers count: $count" >> /tmp/customer_cleanup_log.txt
