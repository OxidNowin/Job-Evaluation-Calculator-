select = document.getElementById("id_around_question");
selectedOptions = [...select];
string = document.getElementById('id_result_dict_1').value;
string1 = string.replace(/'/g, '"');
string1 = string1.replace("False",'"False"');
string1 = string1.replace("True",'"True"');
dict = JSON.parse(string1);
sel = dict.hard_skills;
if(this.sel == "A") {[2,3,4,5,6,7,8].forEach(num => selectedOptions[num].setAttribute("disabled", true));}
if(this.sel == "B") {[3,4,5,6,7,8].forEach(num => selectedOptions[num].setAttribute("disabled", true));}
if(this.sel == "C") {[4,5,6,7,8].forEach(num => selectedOptions[num].setAttribute("disabled", true));}
if(this.sel == "D") {[5,6,7,8].forEach(num => selectedOptions[num].setAttribute("disabled", true));}
if(this.sel == "E") {[6,7,8].forEach(num => selectedOptions[num].setAttribute("disabled", true));}
if(this.sel == "F") {[7,8].forEach(num => selectedOptions[num].setAttribute("disabled", true));}
if(this.sel == "G") {[8].forEach(num => selectedOptions[num].setAttribute("disabled", true));}
    
