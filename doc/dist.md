
A sample distribution packge provides an easy way to ship the sample to a different system for evaluation or demonstration.  

### Build for Distribution:

Run the following script to generate a distribution package:  

```bash
mkdir build
cd build
cmake ..
make
make dist
```

The generated sample distribution package is under the `dist` directory, which you need to distribute to replicate the sample on a different system.  

### Restore Sample:

On a system where you plan to run the sample, run the `restore.sh` script to restore the sample directory structure:  

```bash
./restore.sh
```

### Run Sample:

Follow the usual [sample build and run procedures](../README.md) to invoke the sample. You can alter the [sample options](cmake.md), provided that any such parameter change does not incur an image build. For example, avoid changing `PLATFORM` and `SCENARIO`.   

### See Also:

- [Build Options](cmake.md)   
- [Sample README](../README.md)   

