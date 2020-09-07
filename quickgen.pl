open (INP, "input.txt");

while (<INP>) {
	@fields = split (',',$_);
	$field = $fields[0];
	print "\t\t<div class=\"form-group\">\n" . 
		"\t\t\t{% if form.$field.errors %}<div class=\"alert alert-danger\">{{ form.$field.errors}}</div>{% endif %}\n" . 
		"\t\t\t<label for=\"$field\">$field</label>\n" . 
		"\t\t\t{{ form.$field }}\n" . 
		"\t\t\t<small id=\"$fieldHelp\" class=\"form-text text-muted\">This will be your username to login to the system</small>\n" . 
		"\t\t</div>\n";
}
	
	