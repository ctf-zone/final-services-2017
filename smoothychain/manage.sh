echo "# ------------------------ #"
echo "Available commands:"
echo "[0] Open PostgreSQL console"
echo "[1] Spawn /bin/bash for smoothychain"
echo "[2] Spawn /bin/bash for smoothychain-db"
echo "[Exit] Exit"
echo "# ------------------------ #"
echo "Enter your command: "
while true; do
	read command
	case $command in
	"Exit" | "exit" )
		exit 0
		;;
	"0" )
		docker exec -it smoothychain-db /bin/bash -c "export PGPASSWORD=smoothychain; psql -h localhost -U smoothychain smoothychain"
		;;
	"1" )
		docker exec -it smoothychain /bin/bash
		;;
	"2" )
		docker exec -it smoothychain-db /bin/bash
		;;
	esac
done

