# Grocer - A tool for managing ingredients in a cookbook

Even the best chef needs the right ingredients. Grocer helps you procure the freshest and best tasting ingredients to make a spectacular meal. Your servers will be more delicious than ever. Sorry doesn't support organic or non-GMO at this time.


### TL;DR

1. download package. `cd` into package dir.
2. sudo python setup.py install
3. cd to repo; run grocer_test (foodcritic path defaults to /opt/chef/embedded use -f /opt/chefdk/bin/foodcritic on OSX)

### Overview

Grocer manages the components of a chef cookbook, such as testing for style, syntax, or even functionality (unit tests). Nobody wants to cook with syntax errors or a gnarly regression!
grocer_test is designed for use-cases such as a pre-commit hook on a developer workstation:

```
grocer_test
2015-06-01 14:17:41,537 - grocer - INFO - Starting test process
2015-06-01 14:17:41,537 - grocer - INFO - Running Foodcritic
2015-06-01 14:17:42,442 - grocer - INFO - Running Ruby Syntax Checks
2015-06-01 14:17:42,442 - grocer - INFO - Test process complete!
```

It can also manage resolving dependencies through berkshelf and uploading assets to a chef server for use in a CD/CI pipeline. Notice it will first run the same tests as in grocer_test:

```
grocer_upload
2015-06-01 13:38:33,561 - grocer - INFO - Starting upload process​
2015-06-01 13:38:33,561 - grocer - INFO - Running Foodcritic
2015-06-01 13:38:35,100 - grocer - INFO - Running Ruby Syntax Checks
2015-06-01 13:38:35,100 - grocer - INFO - Testing syntax for file ./metadata.rb
2015-06-01 13:38:35,198 - grocer - INFO - Testing syntax for file ./test/integration/default/default.rb
2015-06-01 13:38:35,296 - grocer - INFO - Testing syntax for file ./test/integration/default/spec_helper.rb
2015-06-01 13:38:35,400 - grocer - INFO - Testing syntax for file ./recipes/default.rb
2015-06-01 13:38:35,493 - grocer - INFO - Testing syntax for file ./attributes/default.rb
2015-06-01 13:38:35,590 - grocer - INFO - Running Berks Install
2015-06-01 13:38:47,453 - grocer - INFO - Running Berks Update
2015-06-01 13:38:59,260 - grocer - INFO - Running Berks Upload
```

### Options

There are a few options you might want to set when running either grocer tool.
It defaults to the locations of the testing binaries that are on the build hosts,
so on a developer workstation you'll likely need to point it somewhere else.
You can use the -h flag to see all the options:

```
optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  The path to the repo. Default is CWD
  -f FOODCRITIC_BIN, --foodcritic_bin FOODCRITIC_BIN
                        The path to the foodcritic binary
  -r RUBY_BIN, --ruby_bin RUBY_BIN
                        The path to the ruby binary
  -l LOG_LEVEL, --log_level LOG_LEVEL
```


### Test Actions

* foodcritic - Runs foodcritic against the specific path, e.g. 'foodcritic .' for CWD
* ruby syntax - Runs the ruby interpreter's built in syntax check tool by invoking the -c flag. First scans the files and directories in the specified path to find ruby files (ending in .rb) and then loops through each one and tests.
* chefspec (unit tests) - coming soon!

### Installation

The tools build job in jenkins will produce an RPM package for installing on RHEL based systems. For OSX systems, you can use python setup tools to install. You'll need some prerequisites if you don't already have them:

```
sudo pip install argparse
```

If you don't have foodcritic or chefpec, the Chef Development Kit is a great way to get it: https://downloads.chef.io/chef-dk/. Then be sure to pass the correct path to the binaries when running it (e.g. "-f /opt/chefdk/bin/foodcritic")
cd grocer
python setup.py install

### Future Enhancements

* Support style tests (rubocop, ruby tailor)
* Validate ERB syntax
* Validate JSON syntax
* Allow for selection of specific tests only on the command line
* Support unit test frameworks for chef such as chefspec

### Source

Its written in python, and the code can be found in the repo called 'grocer'. Pull request, patches welcome!
