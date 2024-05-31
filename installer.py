import urllib.request
import fileinput
from zipfile import ZipFile
import platform
import os

#====================================================================
# STAGE 0	-	DEFINE WORKING VARIABLES
#====================================================================
print("Stage 0: Initialization")
cleanroomBase = "Cleanroom-MMC-instance-0.2.1-alpha.zip"
crurl="https://github.com/CleanroomMC/Cleanroom/releases/download/0.2.1-alpha/Cleanroom-MMC-instance-0.2.1-alpha.zip"
configFile="instance.cfg"
osName=platform.system()
# 0 & 1 - Windows
# 2 & 3 - Mac
# 4 & 5 - Linux/Unix
azulURL=["https://cdn.azul.com/zulu/bin/zulu22.30.13-ca-jdk22.0.1-win_x64.zip","zulu22.30.13-ca-jdk22.0.1-win_x64.zip",
	"https://cdn.azul.com/zulu/bin/zulu22.30.13-ca-jdk22.0.1-macosx_x64.zip","zulu22.30.13-ca-jdk22.0.1-macosx_x64.zip",
	"https://cdn.azul.com/zulu/bin/zulu22.30.13-ca-jdk22.0.1-linux_x64.zip","zulu22.30.13-ca-jdk22.0.1-linux_x64.zip"]
jdkBinary=["/zulu22.30.13-ca-jdk22.0.1-macosx_x64/zulu-22.jdk/Contents/Home/bin/javaw.exe","/zulu22.30.13-ca-jdk22.0.1-macosx_x64/zulu-22.jdk/Contents/Home/bin/java","zulu22.30.13-ca-jdk22.0.1-linux_x64/bin/java"]
# 0 - ZGC
# 1 - ParNewGC
jvmARGs=["JvmArgs=\"-XX:+UnlockExperimentalVMOptions -XX:+UnlockDiagnosticVMOptions -XX:+AlwaysPreTouch -XX:+DisableExplicitGC -XX:NmethodSweepActivity=1 -XX:ReservedCodeCacheSize=400M -XX:NonNMethodCodeHeapSize=12M -XX:ProfiledCodeHeapSize=194M -XX:NonProfiledCodeHeapSize=194M -XX:-DontCompileHugeMethods -XX:MaxNodeLimit=240000 -XX:NodeLimitFudgeFactor=8000 -XX:+UseVectorCmov -XX:+PerfDisableSharedMem -XX:+UseFastUnorderedTimeStamps -XX:+UseCriticalJavaThreadPriority -XX:ThreadPriorityPolicy=1 -XX:+UseZGC -XX:AllocatePrefetchStyle=1 -XX:+ZGenerational\"",
"JvmArgs=\"-Xss4M -Dfile.encoding=GBK -XX:+AggressiveOpts -XX:+UseConcMarkSweepGC -XX:+UseParNewGC -XX:+CMSConcurrentMTEnabled -XX:ParallelGCThreads=8 -Dsun.rmi.dgc.server.gcInterval=1800000 -XX:+UnlockExperimentalVMOptions -XX:+ExplicitGCInvokesConcurrent -XX:MaxGCPauseMillis=50 -XX:+AlwaysPreTouch -XX:+UseStringDeduplication -Dfml.ignorePatchDiscrepancies=true -Dfml.ignoreInvalidMinecraftCertificates=true -XX:-OmitStackTraceInFastThrow -XX:+OptimizeStringConcat -XX:+UseAdaptiveGCBoundary -XX:NewRatio=3 -Dfml.readTimeout=90 -XX:+UseFastAccessorMethods -XX:CMSInitiatingOccupancyFraction=75 -XX:+CMSScavengeBeforeRemark -XX:+UseCMSInitiatingOccupancyOnly\""]


#====================================================================
# STAGE 1	-	DOWNLOADS
#====================================================================
print()
print("Stage 1: Downloading required files")

print("Acquiring Cleanroom MMC template")
urllib.request.urlretrieve(crurl,cleanroomBase)

print("Acquiring JDK 22")
if (osName=="Windows"):
	urllib.request.urlretrieve(azulURL[0],azulURL[1])
if (osName=="Darwin"):
	urllib.request.urlretrieve(azulURL[2],azulURL[3])
if (osName=="Linux"):
	urllib.request.urlretrieve(azulURL[4],azulURL[5])
	


#====================================================================
# STAGE 2	-	EXTRACTIONS
#====================================================================
print()
print("Stage 2: Extraction")

print("Extracting Cleanroom")
zip = ZipFile(cleanroomBase, "r")
zip.extractall()
zip.close()

print("Extracting JDK 22")
if (osName=="Windows"):
	zip = ZipFile(azulURL[1], "r")
	zip.extractall()
	zip.close()
if (osName=="Darwin"):
	zip = ZipFile(azulURL[3], "r")
	zip.extractall()
	zip.close()
if (osName=="Linux"):
	zip = ZipFile(azulURL[5], "r")
	zip.extractall()
	zip.close()

#====================================================================
# STAGE 3	-	JDK 22 SETUP
#====================================================================
print()
print("Stage 3: JDK setup")

print("Notice: This creates a local copy of the Azul JDK 22 for this instance. While good for a single instance, if you make multiple of these, you may want to delete the copies of the JDK and manually configure the JDK used by Prism or MultiMC.")

print("Directing instance config to JDK 22")

if (osName=="Windows"):
	for line in fileinput.input(configFile, inplace = 1): 
		print(line.replace("Replace this with your java path", jdkBinary[0]))
if (osName=="Darwin"):
	for line in fileinput.input(configFile, inplace = 1): 
		print(line.replace("Replace this with your java path", jdkBinary[1]))
if (osName=="Linux"):
	for line in fileinput.input(configFile, inplace = 1): 
		print(line.replace("Replace this with your java path", jdkBinary[2]))

#====================================================================
# STAGE 4	-	FILE CLEANUP
#====================================================================
print()
print("Stage 4: Cleaning up ZIP files to save disk space")

print("Deleting ZIP of Cleanroom template")
os.remove(cleanroomBase)

print("Deleting ZIP of JDK 22")
if (osName=="Windows"):
	os.remove(azulURL[1])
if (osName=="Darwin"):
	os.remove(azulURL[3])
if (osName=="Linux"):
	os.remove(azulURL[5])


#====================================================================
# STAGE 5	-	JVM GARBO COLLECTOR OPTIONS
#====================================================================

print()
print("============================")
print()
print("Java 22 comes with a new garbage collector that performs differently than the original one recommended for Minecraft.")
print("The garbage collector is a vital function of Java that manages memory usage.")
print()
print("The Z Garbage Collector (ZGC) is an experimental and scalable implementation mean for low pause times, even when a modpack is using 7+ GB of RAM. Here's a summary of how it works:")
print()
print("-> Allocates as much RAM as given")
print("-> Will reduce allocation as needed")
print("-> Dumps produce FPS/TPS lag spikes that are usually in the sub-milliseconds, aka the human brain will not notice.")
print("-> May use more memory than default GC")
print("-> Multithreading")
print()
print("If you want to use the ZGC in this instance, type \'y\'. To continue with the default GC, type anything else or press ENTER with the line blank.")
print("============================")
print()

confirmation = input("Use ZGC?  > ")
if (confirmation=="Y" or confirmation=="y"):
	with open(configFile,"a") as file:
		file.write("\n")
		file.write(jvmARGs[0])
else:
	with open(configFile,"a") as file:
		file.write("\n")
		file.write(jvmARGs[1])

print()
print("Now, all you have to do is copy the files from another modpack's .minecraft (or minecraft) folder.\n",+"The forge_early.cfg file shouldn't be replaced, as it contains an important input fix.")
print()


exit = input("Press ENTER to exit ")



