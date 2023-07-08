if [ $1 == "connect" ]
then 
    ssh psaxena@hpc.bits-hyderabad.ac.in
fi
if [ $1 == "post" ]
then
    scp $2 psaxena@hpc.bits-hyderabad.ac.in:/scratch/psaxena
fi
if [ $1 == "get" ]
then
    scp -r psaxena@hpc.bits-hyderabad.ac.in:/scratch/psaxena/$2 ./$3
fi