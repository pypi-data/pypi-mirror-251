As someone who develops real applications or one off programs as well as new functionalities in WolfHECE:
	
- I fork the *HECEPython* repository with git branch so that my developments don't pollute the main branch
- I install Wolf's dependencies with "pip install -r requirements.txt" and "pip install GDAL-3.4.3-cp39-cp39-win_amd64.whl"
- I get an issue in GitLab to track my work (I create it or it is given to me)
- I can use my local copy of WolfHECE (for *.py files; *lib files via the add_path)  (possibly instead of the one installed with pip) with:
    - import sys
    - sys.path.insert(0, r"pathfiletolib")

<h1> Organisation générale - General Structure</h1>
<h2>Fr</h2>

Ce repository Gitlab est destiné à contenir tous les codes Python du HECE.
 
Pour le moment, sa structure est la suivante :
	
- BlenderCityGML : Blenger plugin pour impoter des bâtiments depuis un fichier 3DML
- BlenderGIS : Blender plugin pour traiter des maillages comme des informations SIG (-> petites corrections "nécessaire" par rapport au projet GitHub pour gérer les palettes de couleurs)
- data : répertoire de données (utile notamment pour l'import de valeurs hydrométriques depuis le web)
- debug : code de développement d'une fonctionnalité spécifique
- dike breaching : rupture de digue (cf thèse Vincent Schmitz)
- doc : permet d'y stocker des exemples utiles pour la doc
- doxygen : pages web résultat du traitement automatique du code via Doxygen
- f2py : outil de compilation d'une librairie d'interaction avec le Fortran via Numpy/f2py --> devrait être remplacé par une interaction DLL+CTypes
- pypi_config : fichiers de paramétrisation pour le paquet Pypi.org
- real_apps : applications plus complètes exploitant le paquet wolfhece
- wolfhece : paquet d'outils dans lequel les développements de base doivent se trouver
   - des sous-répertoires thématiques existent déjà, d'autres peuvent être ajoutés	
   - les outils "communs" sont actuellement dans le sous-répertoire principal

Vous pouvez créer des répertoires supplémentaires pour des applications particulières.

La méthode de travail souhaitée est la suivante pour une nouvelle idée/fonctionnalité :
 - créer un ticket
 - créer une branche associée
 - développer
 - demander la fusion

<h2>En</h2>

This Gitlab repository is intended to contain all the HECE Python code.
 
For the moment, its structure is as follows:
	
 - BlenderCityGML: Blender plugin for importing buildings from a 3DML file
 - BlenderGIS: Blender plugin for processing meshes as GIS data (-> some "necessary" corrections compared to the GitHub project for managing colormap).
 - data: data directory (useful especially for importing hydrometric values from the web).
 - debug: development code for a specific functionality.
 - dike breaching: evolution of a breach in a dike (see Vincent Schmitz's PhD).
 - doc: used to store useful examples for documentation.
 - doxygen: web pages resulting from automatic code processing via Doxygen.
 - f2py: tool for compiling a library for interaction with Fortran using Numpy/f2py --> should be replaced by DLL+CTypes interaction.
 - pypi_config: parameterization files for the Pypi.org package.
 - real_apps: more comprehensive applications that utilize the wolfhece package.
 - wolfhece: tools package
   - thematic subdirectories already exist, others can be added.
   - most "common" tools are currently in the main subdirectory.

You can create additional directories for particular applications.

The desired way of working is as follows for a new idea/feature:
 - create an issue
 - create an associated branch
 - code
 - create merge request

 More information on Gitlab (token, ...): https://moodle.hece.uliege.be/mod/wiki/view.php?pageid=298

 <h1>Interaction Fortran-Python - How to Call Fortran from Python </h1>

<h2>Fr</h2>
Il est possible de faire interagir Fortran et Python.

Une voie possible est f2py (https://numpy.org/doc/stable/f2py/). C'est d'ailleurs exploité pour certaines fonctions dans la librairie "wolfpy.pyd", mais cela offre peu de souplesse.

Une autre voie est le module "ctypes" qui est dédié à de l'interaction avec le C, ce que peut faire également nativement le Fortran. 

Comme pour toute interaction multilanguages, le débogage devient cependant plus complexe. Il est en effet nécessaire de disposer d'un outil de débogage en Python (-> VSCode) mais également en Fortran (-> VisualStudio). Le Python doit être tout d'abord lancé et il faut récupérer le PID du process (cd fonction "getpid()" du module "os"). Ce PID est nécessaire pour attacher le débuggeur de Visual Studio au process en cours afin de capter l'appel aux fonctions de la DLL (cf https://stackoverflow.com/questions/27154325/how-to-debug-a-windows-dll-used-inside-python). Il faut bien faire attention à ce que les 2 codes utilisent la même DLL, autrement dit soit adapter le répertoire de sortie de VisualStudio, soit utiliser un chemin absolu vers la librairie compilée dans VSCode.

Dans VSCode, pour que la lecture de la DLL depuis un chemin absolu soit possible, il est utile d'explicitement passer le paramètre "winmode" et de lui imposer une valeur de "0" (source : https://stackoverflow.com/questions/59330863/cant-import-dll-module-in-python).

Un autre problème peut venir du besoin de mémoire de pile (Memory Stack), mémoire notamment exploitée pour les variables locales des routines/fonctions. Comme c'est le Python qui gère le process de base, le paramétrage du projet VisualStudio ne semble pas fonctionner. Il est donc nécessaire de passer par le module "Threading" de Python, seul moyen semble-t-il, d'augmenter la mémoire de pile d'un thread spécifique (cf https://stackoverflow.com/questions/2067637/how-do-i-increase-the-stack-size-in-python).

Une autre approche est de forcer l'allocation de toutes les variables dans la Heap et non dans la Stack. Cela peut se faire via les paramètres du projet Fortran dans "Fortran/Optimization/Heap Arrays" en mettant "0". La conséquence sur le temps de calcul n'a cependant jamais été étudiée.

<h2>En</h2>
Interfacing Fortran and Python is possible.

One viable approach is through the use of f2py (https://numpy.org/doc/stable/f2py/). This technique is actually employed in certain functions within the 'wolfpy.pyd' library, although it provides limited flexibility.

Another way is the 'ctypes' module, specifically designed for interacting with C, which Fortran can naturally interface with as well.

As is customary in multilingual interaction scenarios, debugging becomes significantly more intricate. It is essential to have debugging tools available for both Python (e.g., VSCode) and Fortran (e.g., Visual Studio). Initially, Python must be launched, and the Process ID (PID) of the running instance must be retrieved (accomplished using the 'getpid()' function from the 'os' module). This PID is necessary for attaching the Visual Studio debugger to the running process to capture calls to functions within the DLL (see https://stackoverflow.com/questions/27154325/how-to-debug-a-windows-dll-used-inside-python). Ensuring that both codes utilize the same DLL is crucial, either by adjusting the Visual Studio output directory or specifying an absolute path to the compiled library within VSCode.

In VSCode, to allow for DLL access from an absolute path, it proves advantageous to explicitly set the 'winmode' parameter and set its value to '0' (source: https://stackoverflow.com/questions/59330863/cant-import-dll-module-in-python).

Another potential complication may stem from the necessity for stack memory, typically employed for local variables within routines/functions. Since Python governs the primary process, configuring the Visual Studio project settings may prove ineffective. Therefore, employing Python's 'Threading' module appears to be the sole method of augmenting stack memory for a specific thread (refer to https://stackoverflow.com/questions/2067637/how-do-i-increase-the-stack-size-in-python).

Alternatively, one may opt to force the allocation of all variables in the Heap rather than the Stack. This can be achieved through the Fortran project settings under 'Fortran/Optimization/Heap Arrays' by setting it to '0'. However, it is worth noting that the impact on computation time resulting from this change has not been extensively studied.
