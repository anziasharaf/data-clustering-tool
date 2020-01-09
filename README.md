# Similar Records' clustering tool for databases 

<p>Identification and elimination of duplicate records in huge databases is a major issue faced by every organization involved in big data. The problem of finding exact duplicates can, in large part, be solved using hash tables.The problem is aggravated if we need to find not only the exact duplicates, but also records with differences such as typos or different words or other anomalies. We provide a novel solution to this problem by clustering similar data records based on a threshold and a further verification interface for manually eliminating similar records. We also provide a Malayalam to English transliteration module for processing Malayalam unicode in our records. We use LSH (Locality Sensitive Hashing) to identify similar records bounded by a given threshold. We serve this as a Desktop Application. The main module is written in Python and the UI is made with ElectronJS, thus enabling us to serve the application cross platform.</p>

## Libraries Used

NodeJS : Electron, zerorpc. <br>
Python3: datasketch, zerorpc, ezodf, pandas, nltk.

### Steps for Execution
Clone this repo.
#### For Python3 Part
 * Create a virtual environment for python3.
 * Install the above said python packages.
 * Edit Line 42 of `main.js` and add the location to the virualenv python interpreter.
#### For NodeJS Part
 * Run the installation by setting up `npm install`.

### Authors:
 * Deepu Shaji, Research Assistant ICFOSS
 * Anzi A S, Research Assistant ICFOSS





