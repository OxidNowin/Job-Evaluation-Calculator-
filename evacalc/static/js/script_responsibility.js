select = document.getElementById("id_freedom_action");
options = [...select];
sel = document.getElementById("waterfall_responsibility").value;
alert(sel)
if(this.sel == "A") {[2,3,4,5,6,7,8].forEach(num => options[num].setAttribute("disabled", true));}
if(this.sel == "B") {[3,4,5,6,7,8].forEach(num => options[num].setAttribute("disabled", true));}
if(this.sel == "C") {[4,5,6,7,8].forEach(num => options[num].setAttribute("disabled", true));}
if(this.sel == "D") {[5,6,7,8].forEach(num => options[num].setAttribute("disabled", true));}
if(this.sel == "E") {[6,7,8].forEach(num => options[num].setAttribute("disabled", true));}
if(this.sel == "F") {[7,8].forEach(num => options[num].setAttribute("disabled", true));}
if(this.sel == "G") {[8].forEach(num => options[num].setAttribute("disabled", true));}


document.getElementById("id_nature_impact").addEventListener("change", function() {
  let sel = document.getElementById('id_impact_importance');
  let options = [...sel.options];
  
  options.forEach(elem => elem.removeAttribute("disabled"))

  if(this.value == "N") [1,2,3,4].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "1" || this.value == "2" || this.value == "3" || this.value == "4") [5,6,7,8].forEach(num => options[num].setAttribute("disabled", true))
  
});
