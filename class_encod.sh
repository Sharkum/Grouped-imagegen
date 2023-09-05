for file in $1/*; do
    awk 'FNR==NR {dict[$1]=$2; next} {$1=($1 in dict) ? dict[$1] : $1}1' dict $file > ${file}tmp && mv ${file}tmp $file &
done