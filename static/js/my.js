$(document).ready(function(){
    

    var updateForm = $(".update-data-form")
    var updateFormMethod = updateForm.attr("method")
    var updateFormEndpoint = updateForm.attr("action") 
    
    function displaySubmitting(submitBtn, defaultText, doSubmit){
      if (doSubmit){
        submitBtn.addClass("disabled")
        submitBtn.html("Отправка.")
      } else {
        submitBtn.removeClass("disabled")
        submitBtn.html(defaultText)
      }
      
}
    
    
    updateForm.submit(function(event){
      event.preventDefault()

      var updateFormSubmitBtn = updateForm.find("[type='submit']")
      var updateFormSubmitBtnTxt = updateFormSubmitBtn.text()


      var updateFormData = updateForm.serialize()
      var thisForm = $(this)
        displaySubmitting(updateFormSubmitBtn, "", true)
    $.ajax({
        method: updateFormMethod,
        url:  updateFormEndpoint,
        data: updateFormData,
        success: function(data){
            console.log('Success!')
            updateForm[0].reset()
            $.alert({
                title: "Успешно! ",
                content: "Перейдите на главную страницу, чтобы увидеть результат",
                theme: "modern",
                })
            setTimeout(function(){
                displaySubmitting(updateFormSubmitBtn, updateFormSubmitBtnTxt, false)
}, 500)
        },
        error: function(error){
          console.log(error.responseJSON)
          var jsonData = error.responseJSON
          var msg = ""

          $.each(jsonData, function(key, value){ // key, value  array index / object
            msg += key + ": " + value[0].message + "<br/>"
          })

          $.alert({
            title: "Oops!",
            content: "Что-то пошло не так.",
            theme: "modern",
          })

          

        }
        })
    
    })
  })