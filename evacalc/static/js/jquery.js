$(document).ready(function(){

  // desc1

  $('.desc1-show')
  .click(function(){
    $('.desc1').show();
  });

  $('.desc-close')
  .click(function(){
    $('.desc-container').hide();
  });	
  
  $('.desc-container')
  .click(function(event){
    if(event.target == this) {
      $('.desc-container').hide();
    }
  });

    // desc2

    $('.desc2-show')
    .click(function(){
      $('.desc2').show();
    });

    // desc3

    $('.desc3-show')
    .click(function(){
      $('.desc3').show();
    });

    // desc4

    $('.desc4-show')
    .click(function(){
      $('.desc4').show();
    });

    // desc5

    $('.desc5-show')
    .click(function(){
      $('.desc5').show();
    });

    
    // desc6

    $('.desc6-show')
    .click(function(){
      $('.desc6').show();
    });

    // desc7

    $('.desc7-show')
    .click(function(){
      $('.desc7').show();
    });

    // desc8

    $('.desc8-show')
    .click(function(){
      $('.desc8').show();
    });
  
});