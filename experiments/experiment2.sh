exp=$1
seq=$2
for id in {1..20}; do
    echo "python experiments.py ${exp} ${seq}"
    python experiments.py "${exp}" "${seq}"
    mv "${exp}"_"${seq}"_0.csv "${exp}"_"${seq}"_"${id}".csv
    echo "Performing cleanup"
    rm *wav
    rm *avi
    sleep 5
done

          
