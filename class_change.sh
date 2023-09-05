for file in $1/*; do
    awk '{split($1,a,"."); print a[1], $2, $3, $4, $5}' $file > ${file}tmp && mv ${file}tmp $file &
done