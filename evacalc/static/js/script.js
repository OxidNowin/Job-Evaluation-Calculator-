document.getElementById("id_tech_skills").addEventListener("change", function() {
  let sel = document.getElementById('id_around_question');
  let options = [...sel.options];
  
  options.forEach(elem => elem.removeAttribute("disabled"))
  
  if(this.value == "A") [2,3,4,5,6,7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "B") [3,4,5,6,7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "C") [4,5,6,7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "D") [5,6,7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "E") [6,7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "F") [7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "G") [8].forEach(num => options[num].setAttribute("disabled", true))
  
});
  
document.getElementById("id_around_question").addEventListener("change", function() {
  let sel = document.getElementById('id_free_move');
  let options = [...sel.options];
    
  options.forEach(elem => elem.removeAttribute("disabled"))
    
  if(this.value == "A") [2,3,4,5,6,7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "B") [3,4,5,6,7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "C") [4,5,6,7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "D") [5,6,7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "E") [6,7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "F") [7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "G") [8].forEach(num => options[num].setAttribute("disabled", true))
    
});
  
document.getElementById("id_tech_skills").addEventListener("change", function() {
  let sel = document.getElementById('id_free_move');
  let options = [...sel.options];
    
  options.forEach(elem => elem.removeAttribute("disabled"))
    
  if(this.value == "A") [2,3,4,5,6,7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "B") [3,4,5,6,7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "C") [4,5,6,7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "D") [5,6,7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "E") [6,7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "F") [7,8].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "G") [8].forEach(num => options[num].setAttribute("disabled", true))
    
});

document.getElementById("id_nature").addEventListener("change", function() {
  let sel = document.getElementById('id_impact_importance');
  let options = [...sel.options];
  
  options.forEach(elem => elem.removeAttribute("disabled"))

  if(this.value == "N") [1,2,3,4].forEach(num => options[num].setAttribute("disabled", true))
  if(this.value == "1" || this.value == "2" || this.value == "3" || this.value == "4") [5,6,7,8].forEach(num => options[num].setAttribute("disabled", true))
  
});
