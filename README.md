
## Depndencies

In `lanl-tutorial` run:
* `git clone https://gem5.googlesource.com/public/gem5`
* `virtualenv -p python3 venv`
* `source venv/bin/activate`
* `pip install matplotlib pandas seaborn`

## Building gem5

After cloning gem5 (first step in dependencies), we need to compile gem5. Run
the following commands to compile gem5.
* `cd gem5`
* `scons build/NULL_MESI_Two_Level/gem5.opt -j$(nproc)`

## Running the experiments
