# Jeu de Boules – bedrijfsuitje

Mobiele webapp om een jeu de boules-uitje bij te houden: 4 banen, elk een eigen toernooi van partijen triplette (3 tegen 3), zoveel als er in 90 minuten passen.
Eén HTML-bestand, geen backend, geen login. Alles staat in `localStorage` van de telefoon, per baan (`jdb_baan1` t/m `jdb_baan4`).
Werkt offline na de eerste keer laden (service worker) en is toe te voegen aan het beginscherm.

## Gebruik op de baan

Op het startscherm en onder **Instellingen** staat een korte uitleg "Zo werkt het" voor de spelers.

1. Open de link en kies je baan. De telefoon onthoudt de keuze.
2. Kies de doelscore (9/11/13) en tik op **Start**. Dan begint de klok van het uitje (90 min). Er is geen tijdslimiet per partij: speel partijen tot de tijd op is.
3. Tik per ronde (mène) op **+1 … +6** bij het team dat de ronde wint. **Undo** haalt de laatste ronde weg.
4. Bij het bereiken van de doelscore vraagt de app of de partij afgesloten mag worden.
5. Is de uitjestijd op, dan is de lopende partij de laatste: wie voorstaat wint, gelijk blijft gelijk, daarna volgt de eindstand.
6. Als de tijd op is, of via **Instellingen → Eindstand nu**, verschijnt het eindscherm met **Opslaan als afbeelding**.

### Baan resetten
**Instellingen → Reset baan N** (twee keer bevestigen). Dit wist alleen de stand van die baan op die telefoon.
Verkeerde baan gekozen? **Instellingen → Wissel van baan** (de stand blijft bewaard).

## Klassement
- Saldo per partij = puntenverschil (13–5: winnaars +8, verliezers −8). Gelijkspel = 0.
- Sortering op **totaal saldo** (alle partijen opgeteld), daarna aantal gewonnen partijen, daarna totaal gescoorde punten, daarna onderling resultaat.
- Er is geen maximum aantal partijen. Na partij 4 begint het schema weer bij partij 1.
- Alle banen hebben 6 spelers: iedereen speelt elke partij, niemand rust.
- De lopende partij telt live mee (voorlopig) zodra er gescoord is.
- Een partij die zonder score wordt afgesloten telt als overgeslagen.

## Foto's aanleveren

Zet per speler een vierkante foto (jpg, ±400×400 px) in de juiste map. Precies deze bestandsnamen (kleine letters, geen accenten, streepje bij twee woorden):

| Speler | Bestand |
|---|---|
| Stefen | `players/baan1/stefen.jpg` |
| Hanna G | `players/baan1/hanna-g.jpg` |
| Juliëtte | `players/baan1/juliette.jpg` |
| Joost | `players/baan1/joost.jpg` |
| Gordon | `players/baan1/gordon.jpg` |
| Ardin | `players/baan1/ardin.jpg` |
| Bert | `players/baan2/bert.jpg` |
| Renata | `players/baan2/renata.jpg` |
| Niels | `players/baan2/niels.jpg` |
| Gert | `players/baan2/gert.jpg` |
| Emil | `players/baan2/emil.jpg` |
| Pieter Jan | `players/baan2/pieter-jan.jpg` |
| Myrna | `players/baan3/myrna.jpg` |
| Roxanne | `players/baan3/roxanne.jpg` |
| Bartjan | `players/baan3/bartjan.jpg` |
| Louis | `players/baan3/louis.jpg` |
| Ronnie | `players/baan3/ronnie.jpg` |
| Annika | `players/baan3/annika.jpg` |
| Johan | `players/baan4/johan.jpg` |
| Hanna K | `players/baan4/hanna-k.jpg` |
| Marcel | `players/baan4/marcel.jpg` |
| Bart | `players/baan4/bart.jpg` |
| Abby | `players/baan4/abby.jpg` |
| Roos | `players/baan4/roos.jpg` |

Ontbreekt een foto, dan toont de app een gekleurde cirkel met de eerste letter.
Let op: de site is publiek, dus foto's in deze repo zijn voor iedereen met de link (en zoekmachines) te zien.

## Speelschema's

Berekend met `python3 tools/schema.py` (exhaustief zoeken: elke partij andere teams, minimaal herhaalde teamgenoten,
tegenstanders zo gelijk mogelijk verdeeld, bij 7 spelers rust iedereen hooguit één keer) en hard in `index.html` gezet.
Opnieuw genereren: `python3 tools/schema.py --js` en het `SCHEDULE`-blok in `index.html` vervangen.

```
BAAN 1  (6 spelers: Stefen, Hanna G, Juliëtte, Joost, Gordon, Ardin)
  Partij 1:  Stefen + Hanna G + Juliëtte  vs  Joost + Gordon + Ardin
  Partij 2:  Stefen + Hanna G + Joost  vs  Juliëtte + Gordon + Ardin
  Partij 3:  Stefen + Juliëtte + Gordon  vs  Hanna G + Joost + Ardin
  Partij 4:  Stefen + Joost + Gordon  vs  Hanna G + Juliëtte + Ardin
  Controle: max 2x samen in een team; paren per aantal keer teamgenoot: 0x: 3, 2x: 12
  Partijen gespeeld: Stefen 4, Hanna G 4, Juliëtte 4, Joost 4, Gordon 4, Ardin 4

BAAN 2  (6 spelers: Bert, Renata, Niels, Gert, Emil, Pieter Jan)
  Partij 1:  Bert + Renata + Niels  vs  Gert + Emil + Pieter Jan
  Partij 2:  Bert + Renata + Gert  vs  Niels + Emil + Pieter Jan
  Partij 3:  Bert + Niels + Emil  vs  Renata + Gert + Pieter Jan
  Partij 4:  Bert + Gert + Emil  vs  Renata + Niels + Pieter Jan
  Controle: max 2x samen in een team; paren per aantal keer teamgenoot: 0x: 3, 2x: 12
  Partijen gespeeld: Bert 4, Renata 4, Niels 4, Gert 4, Emil 4, Pieter Jan 4

BAAN 3  (6 spelers: Myrna, Roxanne, Bartjan, Louis, Ronnie, Annika)
  Partij 1:  Myrna + Roxanne + Bartjan  vs  Louis + Ronnie + Annika
  Partij 2:  Myrna + Roxanne + Louis  vs  Bartjan + Ronnie + Annika
  Partij 3:  Myrna + Bartjan + Ronnie  vs  Roxanne + Louis + Annika
  Partij 4:  Myrna + Louis + Ronnie  vs  Roxanne + Bartjan + Annika
  Controle: max 2x samen in een team; paren per aantal keer teamgenoot: 0x: 3, 2x: 12
  Partijen gespeeld: Myrna 4, Roxanne 4, Bartjan 4, Louis 4, Ronnie 4, Annika 4

BAAN 4  (6 spelers: Johan, Hanna K, Marcel, Bart, Abby, Roos)
  Partij 1:  Johan + Hanna K + Marcel  vs  Bart + Abby + Roos
  Partij 2:  Johan + Hanna K + Bart  vs  Marcel + Abby + Roos
  Partij 3:  Johan + Marcel + Abby  vs  Hanna K + Bart + Roos
  Partij 4:  Johan + Bart + Abby  vs  Hanna K + Marcel + Roos
  Controle: max 2x samen in een team; paren per aantal keer teamgenoot: 0x: 3, 2x: 12
  Partijen gespeeld: Johan 4, Hanna K 4, Marcel 4, Bart 4, Abby 4, Roos 4
```

Bij 6 spelers is "12 paren 2× samen, 3 paren nooit" wiskundig het beste wat in 4 rondes kan (de zoektocht controleert alle mogelijkheden).

## Easter eggs
Fanny (verliezen met 0), Carreau! (10% per ronde), Franse commentaarregels (~1 op 5 rondes), Sextuplé! (ronde van 6),
Égalité (gelijke stand), En feu! (3 partijen op rij gewonnen), omgekeerd kroontje voor de hekkensluiter,
en 7× tikken op de titel voor retro-modus.

## Techniek
- `index.html` – de hele app
- `sw.js` – offline cache (verhoog `VERSION` bij een nieuwe release)
- `manifest.json`, `icons/` – beginscherm-icoon (`tools/icons.py`)
- `tools/schema.py` – schemagenerator
