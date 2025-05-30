# created by Tri Nguyen
#
# this script is intended to be used for multiple single files- done by manual input.
# 1. it moves all the welcome email texts out into the root folder
# 2. extracts all the users from the csv files and appends it to a new CSV file

temp_name=TEMP.csv

# removes the temp file if it exists
if [[ -e $temp_name ]]; then
	rm $temp_name
fi

# move text files out
find -type f -name "*.txt" | while read line; do mv "$line" $(pwd); done

# csv generation
find -name "*.csv" -print -quit | xargs cat | grep -E "(version|Name|First)" > $temp_name
find -type f -name "*.csv"  ! -name $temp_name | while read line; do cat "$line" | grep -Ev "(version|Name|First)" >> $temp_name; done