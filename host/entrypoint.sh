
#PID=$!
#
#while [ ! -f /app/minecraft/logs/latest.log ]
#do
#  sleep 1
#done

exec python /app/minecraft/handler.py
