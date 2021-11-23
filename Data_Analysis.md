# Introduction/overview


**QUESTION 1**: Which is the total size of data replicas stored on disk all over the world for the CMS experiment in 2019-2020? How is it splitted between Tier-1 and Tier-2 sites? Which are the prevailing data-tiers?

### 🠊 [Link to OneDrive: "plots/overview/storage_over_time/"](https://liveunibo-my.sharepoint.com/:f:/g/personal/simone_gasperini2_studio_unibo_it/EgnSuna5LPJIj4u8jFJLxDMBCDvw-lIB-CfYdB4RCwR9jA?e=Pl8WaW)


#
**QUESTION 2**: For simulated Analysis Object Data (_AODSIM_, _MINIAODSIM_, _NANOAODSIM_), which is the fraction of data for each Physics Working Group in 2019-2020?

In particular, only Physics Analysis Groups (PAGs) are considered while Physics Objects Groups (POGs) and Detector Performance Groups (DPGs) are merged under the common label "Other PWG".

Note that the PWG assigned to each single dataset is actually the PWG who sent the request to the [Monte Carlo Management](https://cms-pdmv.gitbook.io/project/) (MCM) system to trigger the production of the corresponding dataset. Label "Not found" is used for datasets which have not been successfully found on MCM.

### 🠊 [Link to OneDrive: "plots/overview/sim_data_by_pag/"](https://liveunibo-my.sharepoint.com/:f:/g/personal/simone_gasperini2_studio_unibo_it/EnmAcBJm7RlDoC2TJnTkiegBK3ZH4wJL_naTothJz9UQqg?e=QTLKg9)


#
**QUESTION 3**: For simulated Analysis Object Data (_AODSIM_, _MINIAODSIM_, _NANOAODSIM_), how did the mean size per event change in the time span from 2011 to 2020? Is there a correlation between this mean size and physical quantities like LHC luminosity? Is the mean size measured from the simulated data actually close to the nominal mean size given for each data-tier?

- Nominal size for _AOD_ (Run II) events = <a href="https://www.codecogs.com/eqnedit.php?latex=0.4-0.5&space;\&space;MB/evt" target="_blank"><img src="https://latex.codecogs.com/gif.latex?0.4-0.5&space;\&space;MB/evt" title="0.4-0.5 \ MB/evt" /></a>
- Nominal size for _MINIAOD_ (Run II) events = <a href="https://www.codecogs.com/eqnedit.php?latex=40-50&space;\&space;KB/evt" target="_blank"><img src="https://latex.codecogs.com/gif.latex?40-50&space;\&space;KB/evt" title="40-50 \ KB/evt" /></a>
- Nominal size for _NANOAOD_ (Run II) events = <a href="https://www.codecogs.com/eqnedit.php?latex=1-2&space;\&space;KB/evt" target="_blank"><img src="https://latex.codecogs.com/gif.latex?1-2&space;\&space;KB/evt" title="1-2 \ KB/evt" /></a>

Note that to address this question, each simulated dataset needs to be assigned to the corresponding year of production. To do this, the string "campaign" in the MCM request is used to extract the proper information (e.g. "campaign" = "RunIIAutumn18MiniAOD" --> "year" = "2018").

### 🠊 [Link to OneDrive: "plots/overview/sim_event_size/"](https://liveunibo-my.sharepoint.com/:f:/g/personal/simone_gasperini2_studio_unibo_it/EjB1Wpt5WldAt46EAhDi6UIBEtpSsLvLKP3I53ezIMyISg?e=sO1Gx4)