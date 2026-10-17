# To do:

Andreas:

- Legg til notater i notatet under seksjon 4 om alt som gjøres!!!!!! VELDIG VIKTIG!!!! (hvorfor noe gjøres liksm)
- Legge til accuracy I 3.5
- Intro til prosjekt
- gå gjennom teksten med chat og finn steder hvor vi sier det samme for mange ganger og fjern det
- Methods i raporten 
- Results i raporten


Amy:

- Finere prints og tabellers
- forklar hva gridsearch er (kansje)
- forklare 5.5
- legg linker til i modellene (i 3.2, 3.3, 3.4)
- gjøre plot i 4.3 fra 0.5 - 1 y-aksen

- skrive om kommentarene i md-seksjonene (de som har sånn grå bakgrunn er ikke ferdige kommenttarer)

## Notater til rapport -----------------

# Seksjon 1:

pixel verdiene -> Det gir et hint om hvilke klasser som blir
lette og vanskelige. Trojan 1 og 2 er mye mørkere
enn resten, så de er trolig lette å skille fra de andre,
men kanskje vanskelige å skille fra hverandre. Good,
Backdoor 1 og Backdoor 2 har nesten identisk snitt,
så de kan bli forvekslet. Det kan du sjekke mot confusion
matrix i seksjon 5, og hvis det stemmer, er det en fin
kobling å trekke i rapporten.

CV fold på installer ->
Installer i CV: behold klassen

        Ikke fjern Installer. Oppgaven er å skille mellom alle 10 klassene, så en modell uten Installer løser ikke oppgaven. Men vær ærlig om hva som skjer:

        Med 3 unike bilder får testsettet 1 og treningssettet 2 (stratifiseringen sørger for det).
        Når 2 bilder fordeles på 5 folds, får 3 av foldene ingen Installer-bilder til validering. Du får en advarsel som "The least populated class in y has only 2 members, which is less than n_splits=5". Det er forventet og ikke en feil, så la den stå.
        I folds uten Installer teller ikke klassen med i macro-F1, med mindre modellen feilaktig gjetter Installer på et annet bilde.

        Konsekvensen er at dere har nesten ingen informasjon om hvor godt modellen kjenner igjen Installer. Det skal stå tydelig i rapporten, for eksempel: "After removing duplicates, Installer has only 3 unique images (2 in training, 1 in test). The model's ability to recognise this class can therefore not be reliably estimated, and any score for Installer should be interpreted with great caution."

# Seksjon 2:

splitting av data -> I prosjekt 1 valgte vi en 60/20/20 split, siden da besluttet vi at den passet best.
I dette prosjektet velger vi en 80/20 split med cv fold på testdataen. Mange klasser og
noen svært små. Med 60/20/20 får Installer bare rundt 48 bilder i valideringssettet.
Noen få tilfeldige feil der kan endre F1-scoren for klassen mye. Med CV blir alle
Installer-bildene i treningsdelen brukt til validering én gang, så estimatet blir mer
stabilt.

                Mer data til hver modell. Med 80/20 + CV trenes modellene på 64 % av dataene
                i hver fold, mot 60 % med hold-out, og hele 80 % brukes til validering til sammen.
                Argumentet fra prosjekt 1, "mer data å teste på", holder altså også her. CV gir mer
                data til validering, ikke mindre.

## "In Project 1 we used a 60/20/20 hold-out split. In this project we instead use 5-fold stratified cross-validation on the training set (80 %), while keeping 20 % as a separate test set. With 10 classes, some of them small (e.g. Installer with only 239 images), a single validation set would give noisy estimates, while cross-validation uses all training data for validation and gives a more stable basis for comparing models."

Forbehandling:
StandardScaler er unødvendig fordi alle pikslene allerede ligger på samme skala (0–255). Å dele på 255 gir verdier mellom 0 og 1, og det holder for k-NN og SVM. Random Forest bryr seg ikke om skalering i det hele tatt.

Pipeline trengs bare for å koble en scaler (eller annen forbehandling som lærer fra dataene) sammen med modellen, så den tilpasses på nytt i hver CV-fold. / 255 er en fast konstant og lærer ingenting fra dataene, så det er ingen fare for data leakage, og ingenting å koble sammen.

All features are pixel values on the same scale (0–255), so no standardisation is needed. We only divide by 255 to get values in [0, 1], which helps distance- and margin-based models such as k-NN and SVM. Since 255 is a fixed constant and not computed from the data, this causes no data leakage, and we therefore do not need a Pipeline.

## "We scale pixel values to [0, 1], following the common convention for image data. Since all features share the same scale, this does not change k-NN or Random Forest, but it keeps the values in a standard range for the SVM's gamma parameter."

Metric:
Metrikken brukes to steder i prosjektet. I grid search avgjør den hvilken kombinasjon av modell og hyperparametre som regnes som best. Det er kombinasjonen med høyest gjennomsnittlig score over de fem foldene. Etter det brukes den til å rapportere hvor godt den endelige modellen presterer på testsettet, og det tallet er estimatet vårt på hvordan modellen vil fungere på nye data. Valget av metrikk bestemmer altså hva vi mener med «best». Ulike metrikker kan kåre ulike vinnere: én modell kan få høyest accuracy fordi den er god på de store klassene, mens en annen får høyest macro-F1 fordi den også klarer de små.

I et binært problem finnes det én F1-score. Med ti klasser får vi én F1-score per klasse, og for å sammenligne modeller må disse slås sammen til ett tall. De vanligste måtene er macro (vanlig gjennomsnitt, alle klasser teller likt), weighted (gjennomsnitt vektet etter klassestørrelse, store klasser teller mest) og micro (F1 regnet over alle bildene samlet, som i en enkel flerklasseoppgave som denne blir det samme som accuracy).

Vi valgte metrikk ut fra tre egenskaper ved oppgaven:

Klassene er ubalanserte. Den minste klassen (Installer) har 239 bilder, mens den største (Crypto) har 4 613. Med en slik fordeling kan accuracy og weighted-F1 bli høye selv om modellen gjør det dårlig på de små klassene, fordi de store klassene dominerer.
Alle klassene er like viktige. Å overse en sjelden type malware er like alvorlig som å overse en vanlig. Derfor bør hver klasse telle likt i snittet, og det er det macro-snittet gjør.
Både falske positive og falske negative er kostbare. Hvis malware ikke blir oppdaget, forblir systemet infisert (lav recall). Hvis trygg kode blir merket som malware, må noen sjekke den manuelt (lav precision). F1 er det harmoniske snittet av precision og recall, så den straffer en modell som er dårlig på den ene av dem.

Til sammen gjør dette macro-F1 til den mest passende hovedmetrikken. Vi rapporterer i tillegg accuracy fordi den er intuitiv og lett å kommunisere. Forskjellen mellom de to tallene sier også noe om hvor jevnt modellen presterer på tvers av klassene.

# Seksjon 3:

# Modell valg --------

- desision trees: Dere kjenner det fra prosjekt 1. Alene er det ofte svakt på bilder.

- CNN var et valg om vi ville gjøre det mer komplisert (If you are ambitious about deep learning, you can consider to use libraries such as, for example, PyTorch)
  men siden vi har en max kjøretid på 30 min på CPU-en, blir denne fort urealistisk

- SVM og MLP kan også fort bli treige ved store hyperparamerergrider.
  SVM har en grense i motsatt retning: Den blir treg på veldig store datasett. Derfor passer den godt til størrelsen vår, som er stor nok til å lære mye og liten nok til at SVM er gjennomførbar. SVM kjører på GPU

---

## "We chose SVM over an MLP because SVMs tend to perform well on small to medium-sized datasets such as ours (about 15,000 images), while neural networks usually need larger amounts of data to outperform simpler models. SVM also has fewer hyperparameters to tune and gives deterministic results. At the same time, our dataset is small enough that training an SVM remains feasible on a CPU within the time limit."

Vi velger disse:
_k-NN_ Ser på de mest like treningsbildene (avstand piksel for piksel)
Følsom for støy og forskyvninger i bildet. Alle piksler teller like mye.

_Random_ Mange trær stiller ja/nei-spørsmål om enkeltpiksler
_Forest_ Ser på enkeltpiksler, ikke helheten

_SVM_ Lager glatte skillegrenser mellom klassene i et høydimensjonalt rom
Kan slite når klassene overlapper mye

---

# Seksjon 4:

We select the highest mean macro-F1 before rounding. If scores are exactly equal, we prefer the single model, then standard voting, following the table order. The winner is stored as `final_model` and `final_model_name`. In Section 5, we will fit it on all training data with `final_model.fit(X_train_scaled, y_train)` before evaluating it on the test set. Cross-validation fits copies and does not leave the ensembles fitted.

# Seksjon 5:
Hypotesen holder delvis:

Den støttes: De to likeste parene er også blant de som blir forvekslet mest. Good–Backdoor 2 er det paret med flest feil av alle.
Unntak: Backdoor 1 og Downloader er det tredje likeste paret, men blir nesten aldri forvekslet.
Overraskelse: Good–Crypto har 40 feil, men var ikke blant de fem likeste parene.
Det største mønsteret: Good er med i nesten alle de store feilene og har en recall på bare 19 %. Trygge filer ligner tydeligvis på mange ulike typer malware. Det er et viktig funn, fordi det betyr mange falske alarmer for alvene.

Store klasser får flere feil bare fordi de har flere bilder. Crypto har 734 testbilder og Downloader 118.

The Good class is part of 4 of the 5 most confused pairs. This suggests that Good is hard to classify in general, not only because it looks like one spesific class. 


KILDER:
valg av SVM vs MLP -> https://www.geeksforgeeks.org/machine-learning/support-vector-machines-vs-neural-networks/

plt.legend -> https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html

math plot patch -> https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Patch.html

grid cross val score -> https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html

cv -> https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedKFold.html

modelene
knn -> https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html

random forest -> https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html

svc -> https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
