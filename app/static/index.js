function renderTable(table_data)  {
    return;
}

function display_modal(organisation_name, id, row_id) {
    $('#org_name').text(organisation_name);
    $('#myModal').modal('show');
    $('#delete_button').attr("onclick","delete_organisation(" + id + "," +  row_id + ")");
}

function edit_row(button, id) {
    console.log(button);
    var currentTD = button.parents('tr').find('td');

    if (button.html() == 'Edit') {
          currentTD = button.parents('tr').find('td');
          console.log(typeof currentTD);
          $.each(currentTD, function () {
              if($(this).prop('contenteditable') === "false") {
                    $(this).css("border", "1px solid #ff0000")
                    $(this).prop('contenteditable', true)
              }

          });
    } else {
         updatedInformation = [];
         $.each(currentTD, function () {
              if($(this).prop('contenteditable') === "true") {
                  $(this).css("border", "1px solid #ffffff")
                  $(this).prop('contenteditable', false)
                  updatedInformation.push($(this).html());
              }
          });
          console.log(updatedInformation);
          edit_organisation(updatedInformation, id);


    }

    button.html(button.html() == 'Edit' ? 'Submit' : 'Edit')
}

function edit_organisation(information, id) {
     var data = {'info' : information};
     console.log(data);
     $.ajax({
        url: "edit/" + id,
        type: 'POST',
        data: {'info' : information},
        success: function(res) {
            alert("Done");

        }
    });
}

function delete_organisation(id, row_id) {
    $.ajax({
        url: "delete/" + id,
        type: 'GET',
        dataType: 'json', // added data type
        success: function(res) {
            if(res["is_deleted"] === true) {
                $('#'+ row_id).remove();
            }
            else{
                alert("Unable to complete deletion");
            }

        }
    });
}

function display_completion_modal(id) {
    $('#completion_id').text(id);
    $("#completion_modal").modal("show");
}

function display_creation_modal() {
    $("#creation_modal").modal("show");
}

function create_organisation() {
    var form_data = new FormData($("#create_form"));
    console.log(form_data);
}