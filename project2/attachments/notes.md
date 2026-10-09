# To do:
- se gjennom alle forelesningene og se hvilke modeller vi har lært
- velge modellene vi skal bruke videre
- 

- skrive om kommentarene i md-seksjonene (de som har sånn grå bakgrunn er ikke ferdige kommenttarer)


## Notater til rapport -----------------
# Modell valg:

- desision trees: Dere kjenner det fra prosjekt 1. Alene er det ofte svakt på bilder.

- CNN var et valg om vi ville gjøre det mer komplisert (If you are ambitious about deep learning, you can consider to use libraries such as, for example, PyTorch)
men siden vi har en max kjøretid på 30 min på CPU-en, blir denne fort urealistisk

- SVM og MLP kan også fort bli treige ved store hyperparamerergrider. 
SVM har en grense i motsatt retning: Den blir treg på veldig store datasett. Derfor passer den godt til størrelsen vår, som er stor nok til å lære mye og liten nok til at SVM er gjennomførbar.
---
"We chose SVM over an MLP because SVMs tend to perform well on small to medium-sized datasets such as ours (about 15,000 images), while neural networks usually need larger amounts of data to outperform simpler models. SVM also has fewer hyperparameters to tune and gives deterministic results. At the same time, our dataset is small enough that training an SVM remains feasible on a CPU within the time limit."
---

Vi velger disse:
*k-NN*	Ser på de mest like treningsbildene (avstand piksel for piksel)	
        Følsom for støy og forskyvninger i bildet. Alle piksler teller like mye.

*Random* Mange trær stiller ja/nei-spørsmål om enkeltpiksler	
*Forest* Ser på enkeltpiksler, ikke helheten

*SVM*	Lager glatte skillegrenser mellom klassene i et høydimensjonalt rom	
        Kan slite når klassene overlapper mye


# Seksjon 1:
pixel verdiene -> Det gir et hint om hvilke klasser som blir 
                lette og vanskelige. Trojan 1 og 2 er mye mørkere 
                enn resten, så de er trolig lette å skille fra de andre, 
                men kanskje vanskelige å skille fra hverandre. Good, 
                Backdoor 1 og Backdoor 2 har nesten identisk snitt, 
                så de kan bli forvekslet. Det kan du sjekke mot confusion 
                matrix i seksjon 5, og hvis det stemmer, er det en fin 
                kobling å trekke i rapporten.


# Seksjon 3:

# Seksjon 4:

# Seksjon 5:


KILDER:
valg av SVM vs MLP -> https://www.geeksforgeeks.org/machine-learning/support-vector-machines-vs-neural-networks/ 
 

plt.legend -> https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html

math plot patch -> https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Patch.html