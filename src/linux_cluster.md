# Koble til og bruke NTNU sin Linux-cluster for å gjøre beregninger med Python.

Åpne kommandolinjen. Sørg for at ssh er installert.

Logg inn på ntnu sine sider:
```
ssh -X login.stud.ntnu.no -l aurorasg
``` 
 Logg så inn på clusteren:

```
ssh -X  hpc-2.phys.ntnu.no
```
Eller for Idun:
```
ssh -X  idun-login1.hpc.ntnu.no
```
Dette er en Linux-cluster og du kommuniserer til den via kommandolinjen.
Naviger til arbeidsområdet:
```
cd /work/username
``` 
For å se innholdet kan du bruke denne kommandoen:
```
ls
```
For å lese en tekstfil:
```
cat file/path.txt
```
For å redigere en tekstfil kan du bruke det enkle tekstredigeringsprogrammet nano:
```
nano file/path.txt
```
Programmer lastes inn ved å velge en modul. Det er mange forskjellige moduler. For å bruke den nyeste versjonen av Python med en del innstallerte pakker last inn Anaconda modulen:

Fysikk:
```
module load eb
module load Anaconda3    
``` 
Idun
```
 module load Anaconda3/2018.12
``` 

Da kan du også installere nye pakker ved å bruke pip:

```
pip install --user package_name 
``` 

Fildeling mellom din laptop hjemme og NTNU cluster kan være litt komplisert og ta lang tid, men en grei måte å gjøre det på er ved å bruke et `github` repository som du laster opp til og laster ned filene fra. Pass på å legge til en `.gitignore` fil i hovedmappen som forteller hvilke filer som IKKE skal deles. Det er lurt dersom du har store datafiler du ikke trenger å dele. Det er også en maksgrense for filstørrelser på GitHub.