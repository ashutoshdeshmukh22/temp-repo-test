$(document).ready(function () {

  const csrftoken = CSRF_TOKEN;

  var IndCurr = $(".IndCurr");

  // setInterval( function(){

  $(".IndCurr").each(function (i) {
    var curr_data = $(this).text()
    // console.log(toIndianCurrency( parseFloat(curr_data)))
    $(this).text(toIndianCurrency(parseFloat(curr_data)))
  });


  // }, 1000 )


  $(".save_script_data").on("click", function () {

    var script_code = $(this).attr("data-script-code");
    var script_id = $(this).attr("data-script-id");
    var multiplier = $(".multiplier_" + script_code).val();
    var lot_size = $(".lot_size_" + script_code).val();

    if (multiplier != "" || lot_size != "") {
      var settings = {
        "url": "/api/v1/update_script",
        "method": "POST",
        "timeout": 0,
        "headers": {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        "data": JSON.stringify({
          "script_code": script_code,
          "multiplier": multiplier,
          "lot_size": lot_size,
          "script_id": script_id,
        }),
      };

      $.ajax(settings).done(function (response) {
        console.log(response);
        if (response['status'] == "success") {
          alert("Script Updated Successfully!!!");
          // location.reload();
        }

      });
    } else {
      alert("You must have to specified value for it.")
    }



  });

  $(".remove_script_from_app").on("click", function () {
    var script_id = $(this).attr("data-script-id");

    var settings = {
      "url": "/api/v1/remove_script?script_code=" + script_id,
      "method": "GET",
      "timeout": 0,
      "headers": {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      }
    };

    $.ajax(settings).done(function (response) {
      location.reload();
    });

    // location.reload();
  });

  $(".update_access_token").on("click", function () {
    var AccessToken_id = $(".AccessToken_id").val();

    if (AccessToken_id != "") {

      var settings = {
        "url": "/api/v1/token/add",
        "method": "POST",
        "timeout": 0,
        "headers": {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        "data": JSON.stringify({
          "request_id": AccessToken_id
        }),
      };

      $.ajax(settings).done(function (response) {
        //console.log(response);
        alert("Access Token Updated Successfully!!!");
        location.reload();
      });

    } else {
      alert("Please add access token.");
    }
  });

  $(".save_app_settings").on("click", function () {

    var field_app_name = $(".field_app_name").val();
    var field_app_status = $(".field_app_status").is(':checked');
    var field_transaction_status = $(".field_transaction_status").is(':checked');
    var field_app_hostname = $(".field_app_hostname").val();

    var field_app_limit = $(".field_app_limit").val();
    var field_app_canSubAdminCreateUser = $(".field_app_canSubAdminCreateUser").is(':checked');

    var settings = {
      "url": "/api/v1/settings/update",
      "method": "POST",
      "timeout": 0,
      "headers": {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      "data": JSON.stringify({
        "app_name": field_app_name,
        "app_status": field_app_status,
        "transaction_status": field_transaction_status,
        "hostname": field_app_hostname,
        "initial_limit": field_app_limit,
        "canSubAdminCreateUser": field_app_canSubAdminCreateUser
      }),
    };

    $.ajax(settings).done(function (response) {
      console.log(response);
      location.reload();
    });

  });


  // Settings
  // Function to filter expiry dates based on the selected symbol
  $("#symbol").on("change", function () {
    const symbol = document.getElementById('symbol').value;
    const expirySelect = document.getElementById('script_expiry');
    expirySelect.innerHTML = '<option value="" selected disabled >Expiry Date</option>'; // Clear existing options

    if (symbol) {
      $.ajax({
        "url": "/script/get?symbol=" + symbol,
        "headers": {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        "method": "GET",
        success: function (result) {
          if (result != "Please refresh script list") {
            const uniqueExpiryDates = [...new Set(result.filter(item => item.tradingSymbol === symbol).map(item => item.expiry))];
            uniqueExpiryDates.forEach(date => {
              const filteredItems = result.filter(item => item.tradingSymbol === symbol && item.expiry === date);
              const uniqueCodes = [...new Set(filteredItems.map(item => item.scripCode))];

              uniqueCodes.forEach(code => {
                const option = document.createElement('option');
                option.value = code; // Set the value as the unique code
                option.textContent = `${symbol} (${code}) - ${date}`; // Display symbol, code, and date
                expirySelect.appendChild(option);
              });
            });
          } else {
            alert("Please refresh script list");
          }
        }
      });
    }
  });

  $("#script_expiry").on("change", function () {
    const symbol = document.getElementById('symbol').value;
    const expiry = document.getElementById('script_expiry').value;
    const codeInput = document.getElementById('code');

    // if (symbol && expiry) {
    //   const selectedItem = data.find(item => item.symbol === symbol && item.expirydate === expiry);
    //   codeInput.value = selectedItem ? selectedItem.code : '';
    // }
  });

  $("#addScript").on("click", function () {
    const scriptCode = document.getElementById('script_expiry').value;

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (scriptCode) {
      $.ajax({
        "url": "/script/add",
        "method": "POST",
        "headers": {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        "data": JSON.stringify({ "scriptCode": scriptCode }),
        "success": function (result) {
          if (result == "success") {
            location.reload();
          } else {
            alert(result);
          }
        }
      });
    }
  });

  $("#RefreshScript").on("click", function () {

    $.ajax({
      "url": "/scripts/refresh",
      "method": "POST",
      "headers": {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      "data": {},
      "success": function (result) {
        alert(result);
      }
    });
  });




  /**
   *  Single user page 
   */

  var single_user_edit_info = $(".single_user_edit_info");
  var edit_user_info_update_btn = $(".edit_user_info_update_btn");
  var mark_as_in_active_user = $(".mark_as_in_active_user");


  if (mark_as_in_active_user) {
    mark_as_in_active_user.on("click", function () {
      var edit_info_client_id = $(".edit_info_client_id").val();
      var settings = {
        "url": "/api/v1/user/edit",
        "headers": {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        "method": "POST",
        "timeout": 0,
        "headers": {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
          //"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3MTY1NDA1LCJpYXQiOjE2ODcwNzkwMDUsImp0aSI6IjRiNGJiMjVkYzU4MTQxMDBiYjk4ZjEwMmZlNWM4OTYwIiwidXNlcl9pZCI6MX0.9jV7saIPNVgzPrXUOWpn7dBkNs0Cxj8jb9IHKGraMz0"
        },
        "data": JSON.stringify({
          "username": edit_info_client_id,
          "is_active": false,
        }),
      };

      $.ajax(settings).done(function (response) {
        window.location.href = "/users/";
      });

      return false;
    });
  }



  if (edit_user_info_update_btn) {
    edit_user_info_update_btn.on("click", function () {
      var edit_info_firstname = $(".edit_info_firstname").val();
      var edit_info_email = $(".edit_info_email").val();
      var edit_info_phone = $(".edit_info_phone").val();
      var edit_info_limit = $(".edit_info_limit").val();
      var edit_info_client_id = $(".edit_info_client_id").val();


      var settings = {
        "url": "/api/v1/user/edit",
        "method": "POST",
        "headers": {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        "timeout": 0,
        "data": JSON.stringify({
          "username": edit_info_client_id,
          "name": edit_info_firstname,
          "email": edit_info_email,
          "phone": edit_info_phone,
          "limit": edit_info_limit,
          "note": "This is test note"
        }),
      };

      $.ajax(settings).done(function (response) {
        console.log(response);
        location.reload();
      });

    });
  }

  if (single_user_edit_info) {
    single_user_edit_info.on("click", function () {
      $(".edit_info_firstname").prop("disabled", false);
      $(".edit_info_email").prop("disabled", false);
      $(".edit_info_phone").prop("disabled", false);
      $(".edit_info_limit").prop("disabled", false);
      return false;
    });
  }




  /** JS For User Module */

  var dataTable;

  if ($(".datatable")) {

    var myDate = new Date();
    // myDate.setFullYear(2023);
    // myDate.setMonth(5);
    // myDate.setDate(9);

    console.log("myDate.getDay()", myDate.getDay());

    current_day_name = "friday";
    // if( myDate.getDay() == 5 ){
    //   current_day_name = "friday";
    // }


    dataTable = $('.datatable').DataTable({
      "dom": 'Bfrtip',
      buttons: [
        {
          extend: 'excel',
          className: 'btn btn-primary float-right export_button_custom_datatable ' + current_day_name,
          footer: true
        }
      ],

      footerCallback: function (row, data, start, end, display) {
        var api = this.api();

        if ($(".is_s_trasaction").length > 0) {

          // Sum of Column 5
          $(api.column(5).footer()).html(
            api.column(5).data().reduce(function (a, b) {
              // console.log("a => ", a)
              // console.log("b => ", b )
              return parseInt(a) + parseInt(b);
            }, 0)
          );

          // Sum of Column 4
          $(api.column(4).footer()).html(
            api.column(4).data().reduce(function (c, d) {
              // return c + d;
              // console.log("C => ", c)
              // console.log("D => ", $(d).text() )
              return parseInt(c) + parseInt($(d).text());
              // return parseInt(c.replace(/[^0-9\-]/g, "")) + parseInt(d.replace(/[^0-9\-]/g, ""));
            }, 0)
          );

        }




      }

      // }
    })



    // dataTable.column(9).data("test").draw();

  }

  // $(document).ready(function () {
  //   $(".datatable").table2excel({
  //     exclude: ".noExport",
  //     filename: "Transactions.xlsx",
  //   });
  // });

  $(document).ready(function () {
    $(".export_button_custom").click(function () {
      let table = document.getElementsByTagName("table");
      console.log(table);
      // debugger;
      TableToExcel.convert(table[0], {
        name: `transactions.xlsx`,
        sheet: {
          name: 'transactions'
        }
      });
    });
  });


  /** Web Socket Data Code Start */

  // $('.datatable').DataTable();


  var access_token = "eyJ0eXAiOiJzZWMiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJneTZOU2xzeXhrQW94dlpLWE96b053L0pFOVZGaG1OVDB0YjUwTFJBYWgyMzNWMzBpOTJGUm5aRnVwL1J3MzF1bHFwTmw1NUN4YlVQWmQybkc0Qnk0cTRlZ3lmdElrejJYWi8zUm5yYnF0ZWlzQzhHYkdaRTRTQmpvcU8rVFptWHNXNzQ2c1hIZExvTHY3bjVzdUVLYUxmcWgrOUUvSlE5SHlLMlg1WWlJOVk9IiwiaWF0IjoxNjg4ODA4NDE1LCJleHAiOjE2ODg4OTQ4MTV9.W1SVjwIx_4glIpo1PjmiUUNBQRbGAXu9hZVRjaXnkYs";
  var api_key = "2ndfeZojiGUjxuBaHvjsvwG7UIS4CZhH";
  var ws = new WebSocket("wss://stream.sharekhan.com/skstream/api/stream?ACCESS_TOKEN=" + access_token + "&API_KEY=" + api_key);

  ws.onopen = function () {
    console.log("Connected to WebSocket server");

    ws.send(JSON.stringify({
      "action": "subscribe",
      "key": ["feed"],
      "value": [""]
    }));

    ws.send(JSON.stringify({
      "action": "feed",
      "key": ["full"],
      "value": ["MX245896"]
    }));

    // console.log( "Data", data_from_api );

  };


  ws.onmessage = function (event) {
    var message = event.data;
    // Call a function to process the received message
    if (message != "heartbeat") {
      processMessage(message);

      jsonparse_data = JSON.parse(message);
      console.log("Bid Price : ", jsonparse_data.data[0].bidPrice);
      const newColumnData = jsonparse_data.data[0].bidPrice; // Replace 'columnData' with the actual field name in your data object
      updateColumnData(9, newColumnData); // Replace '1' with the index of the column you want to update
    }
  };

  function updateColumnData(columnIndex, newData) {
    dataTable.column(columnIndex).data(newData).draw();
  }



  function processMessage(message) {
    console.log("Data Without Filter", message);
    var message_json = JSON.parse(message);
    console.log("Received message: ", message_json);
    // Do further processing or use the message data as needed
    // For example, you can update the UI, perform calculations, etc.
  }


  /** Web Socket Data Code end  */


  $('.deactivate_checkbox').on('click', function () {
    var checkbox = $(this);
    var user_id = checkbox.attr('data-id');
    var modaldiv = checkbox.is(':checked') ? $("#activate_user") : $("#deactivate_user");
    var current_state = checkbox.is(':checked') ? "activate_user" : "deactivate_user";
    //var action = checkbox.is(":checked") ? true : false;

    $(".clientid").text(user_id);
    var data;

    // 
    custom_confirm(modaldiv, function (result) {
      var action = checkbox.is(':checked');
      var data = [];

      // if( !result ){
      //   checkbox.prop('checked', result ? action : !action);
      // }

      if (result && current_state == "activate_user") { // call ajax to activate or deactive based on whatever popup is open.
        // call 
        // item id 
        // status ( true / false )
        // data['user_id'] = user_id; 
        // data['status'] = true;

        data = { username: user_id, is_active: true };

        console.log("data", JSON.stringify(data));

        var settings = {
          "url": "/api/v1/user/edit",
          "method": "POST",
          "headers": {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          "timeout": 0,
          "data": JSON.stringify(data),
        };

        $.ajax(settings).done(function (result, status, jqXHR) {
          console.log('response', result);
          console.log('status', status);
          console.log('jqXHR', jqXHR);
          if (status == "success") {
            console.log("Response", result);
            // var action = checkbox.is(":checked") ? true : false;
            console.log('action', action);
            checkbox.prop('checked', result ? !action : action);
            location.reload();

            // return true;
          } else {
            console.log("API Status", status);
            console.log("API Issues", jqXHR);
          }
        });

        // $.ajax({
        //     url: "/api/v1/user/edit",
        //     method: "POST",
        //     data: JSON.stringify(data),
        //     dataType: 'json',
        //     contentType: "application/json",
        //     success: function(result,status,jqXHR ){
        //           //Do something
        //           console.log("result", result);
        //           // if( status == "200" ){
        //           //   console.log( "Response", result );
        //           // }else{
        //           //   var action = checkbox.is(":checked") ? true : false;
        //           //   console.log( "API Status", status );
        //           //   console.log( "API Issues", jqXHR );
        //           // }

        //     },
        //     error(jqXHR, textStatus, errorThrown){
        //         //Do something
        //         var action = checkbox.is(":checked") ? true : false;
        //         console.log( "jqXHR", jqXHR );
        //         console.log( "textStatus", textStatus );
        //         console.log( "errorThrown", errorThrown );
        //     }
        // }); 

      }

      if (result && current_state == "deactivate_user") {

        data = { username: user_id, is_active: false };

        console.log("data", JSON.stringify(data));

        var settings = {
          "url": "/api/v1/user/edit",
          "method": "POST",
          "timeout": 0,
          "headers": {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
            //"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3MTY1NDA1LCJpYXQiOjE2ODcwNzkwMDUsImp0aSI6IjRiNGJiMjVkYzU4MTQxMDBiYjk4ZjEwMmZlNWM4OTYwIiwidXNlcl9pZCI6MX0.9jV7saIPNVgzPrXUOWpn7dBkNs0Cxj8jb9IHKGraMz0"
          },
          "data": JSON.stringify(data),
        };

        $.ajax(settings).done(function (result, status, jqXHR) {
          console.log('response', result);
          console.log('status', status);
          console.log('jqXHR', jqXHR);


          if (status == "success") {
            console.log("Response", result);
            // var action = checkbox.is(":checked") ? true : false;
            console.log('action', action);
            checkbox.prop('checked', result ? !action : action);
            location.reload();

            // return true;
          } else {
            // var action = checkbox.is(":checked") ? true : false;
            // checkbox.prop('checked', result ? action : !action);
            console.log("API Status", status);
            console.log("API Issues", jqXHR);
          }
        });

        // $.ajax({
        //     url: "/api/v1/user/edit",
        //     method: "POST",
        //     data: JSON.stringify(data),
        //     dataType: 'json',
        //     contentType: "application/json",
        //     success: function(result,status,jqXHR ){
        //           //Do something
        //           console.log("result", result);
        //           // if( status == "200" ){
        //           //   console.log( "Response", result );
        //           // }else{
        //           //   var action = checkbox.is(":checked") ? true : false;
        //           //   console.log( "API Status", status );
        //           //   console.log( "API Issues", jqXHR );
        //           // }

        //     },
        //     error(jqXHR, textStatus, errorThrown){
        //         //Do something
        //         var action = checkbox.is(":checked") ? true : false;
        //         console.log( "jqXHR", jqXHR );
        //         console.log( "textStatus", textStatus );
        //         console.log( "errorThrown", errorThrown );
        //     }
        // }); 

      }

      //checkbox.prop('checked', result ? action : !action);

    });

    return false;
  });

  function custom_confirm(modal, callback) {
    modal.modal({
      backdrop: 'static',
      keyboard: true,
      show: true
    });
    modal.modal('show');

    modal.find(".ok").off().click(function () {
      modal.modal('hide');
      callback(true);
    });

    modal.find(".cancel").off().click(function () {
      modal.modal('hide');
      callback(false);
    });
  }

  var is_check_new_transaction = $(".check_new_transaction");

  if (is_check_new_transaction.length) {
    setInterval(
      function () {
        var settings = {
          "url": "/api/v1/fetch_active_transactions/",
          "method": "POST",
          "timeout": 0,
          "headers": {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          }
        };

        $.ajax(settings).done(function (response) {
          console.log(response);
          if (response.success) {
            if (response.data.length > 0) {
              console.log("New Transaction found, Reloading page...!");
              location.reload();
            } else {
              console.log("Waiting for new transaction. ");
            }
          }
        });
      },
      60000
    )
  }

});


function squareoftransactions(data) {
  csrftoken = CSRF_TOKEN;

  var settings = {
    "url": "/api/v1/SquaredOffTransaction/all",
    "method": "POST",
    "timeout": 0,
    "headers": {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    "data": JSON.stringify(data)
  };

  $.ajax(settings).done(function (response) {
    console.log(response.success);
    if (response.success) {
      // window.reload();
      location.reload();
    }

  });
}

const toIndianCurrency = (num) => {
  const curr = num.toLocaleString('en-IN', {
    style: 'currency',
    currency: 'INR'
  });
  // return curr;
  return num;
};

// function callback_toIndianCurrency(num){
//   const curr = num.toLocaleString('en-IN', {
//       style: 'currency',
//       currency: 'INR'
//     });
//   return curr;
// }