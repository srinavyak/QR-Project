// Global Variables
var mainBodyData = [],
    searchResultsData = [],
    actionColumnsData = [];
var tableName = '',
    searchField = '',
    columns = 1,
    actionColumns = 0,
    recordsPerPage = 10,
    currentPageNumber = 1;

// This Method should be called on the Page Load i.e. use the document.ready
function onPageLoad(paramSourceData, paramTableName, paramColumns, paramActionColumns,
    paramActionColumnsData, paramCurrentPageNumber, paramsearchField) {
    //debugger;
    console.log(paramSourceData);
    // Storing the val data to the global variable, so we can re-use it for future use
    tableName = paramTableName;
    mainBodyData = paramSourceData;
    columns = paramColumns;
    actionColumns = paramActionColumns;
    actionColumnsData = paramActionColumnsData;
    searchField = paramsearchField;

    tableBinding(paramCurrentPageNumber);
    applyPagination();
}

// This Method is used to bind the body data to the table
function tableBinding(PageNumber) {

    //debugger;

    var recordNumber = "";
    var Rows = [];
    currentPageNumber = parseInt(PageNumber);

    if (PageNumber != 1)
        recordNumber = PageNumber - 1;

    //// The below if condition will work on search result
    //if ($("#txtSearch").val() != "" && $("#txtSearch").val() != undefined) {
    //    bindSearchResultsToTableBody(PageNumber);
    //    return;
    //}

    Rows = getFirst_LastRow(recordNumber, currentPageNumber);

    prepareAndBindTableUsingHTMLScript(tableName, Rows, mainBodyData);
    showRecords(Rows);

}

// This Method is used to prepare the HTML script required to bind to table Body
function prepareAndBindTableUsingHTMLScript(tableName, Rows) {

    //debugger;

    var totalColumns = columns.length + actionColumns,
        colSpan1 = (totalColumns % 2) > 0 ? (totalColumns % 2) + 1 : (totalColumns / 2),
        colSpan2 = (totalColumns - colSpan1);

    var tableData = '';

    // Table Head

    if ($("#txtSearch").val() == "" || $("#txtSearch").val() == undefined) {

        $('#' + tableName).empty();

        tableData = '<thead>' +
            '<tr>' +
            '<th colspan="' + colSpan1 + '" style="text-align:right;">Search</th>' +
            '<th colspan="' + colSpan2 + '"><input type="text" id="txtSearch" class="form-control" placeholder="Search" style="margin-bottom:0px;" onkeyup="searchData();"/></th>' +
            '</tr>';

        tableData += '<tr style="background-color:#6777ef;color:#fff;">';

        tableData += prepareTableHeadingScript();

        tableData += '<th colspan="' + actionColumns + '" style="text-align:center">Action</th>' +
            '</tr></thead>';
    } else {
        $("#" + tableName).find("tbody").empty();
    }

    // Table Head Close

    // Table Body 

    tableData += '<tbody>';

    tableData += prepareTableBodyScript(Rows[0], Rows[1]);

    tableData += '</tbody>';

    // Table Body Close

    $('#' + tableName).append(tableData);
}

function prepareTableHeadingScript() {

    //debugger;

    var data = "",
        headingColumns = columns;

    for (var v = 0; v < headingColumns.length; v++) {
        data += '<th>' + headingColumns[v] + '</th>';
    }

    return data;

}

function prepareTableBodyScript(bodyStartRow, bodyLastRow) {

    //debugger;

    var sourceData = searchResultsData.length != 0 ? searchResultsData : mainBodyData;
    var data = '';

    for (var i = bodyStartRow; i <= bodyLastRow; i++) {

        if (i <= bodyLastRow && i < sourceData.length) {

            // Body Data Columns
            for (var v = 0; v < columns.length; v++) {
                if (v == 0) {
                    // for ID Column, always 1st column should be ID column
                    data += '<tr id="tr_' + sourceData[i][columns[v]] + '">';
                    data += '<td><label id="td_' + columns[v] + '_' + sourceData[i][columns[0]] + '">' + (i + 1) + '</label></td>';
                } else {
                    data += '<td><label id="td_' + columns[v] + '_' + sourceData[i][columns[0]] + '">' + sourceData[i][columns[v]] + '</label><input type="text" class="form-control tempname' + columns[v] + '_' + sourceData[i][columns[0]] + '" name="tempname' + columns[v] + '_' + sourceData[i][columns[0]] + '" id="tempname_' + sourceData[i][columns[v]] + '" value="' + sourceData[i][columns[v]] + '" placeholder="TemplateName" style="display:none;" required></td>';
                }

            }

            // Action Columns Data
            for (var v = 0; v < actionColumnsData.length; v++) {

                if (actionColumnsData[v] == 'form') {
                    data += '<td id="td_form_' + sourceData[i][columns[0]] + '" ><button onclick="formOperation(' + sourceData[i][columns[0]] + ')" type="button" class="btn btn-round btn-success bg-gradient-success edit" id="edit_' + sourceData[i][columns[0]] + '"  style="background-color:#0078d7">Form</button></td>';
                } else if (actionColumnsData[v] == 'uploaddoc') {
                    data += '<td id="td_uploaddoc_' + sourceData[i][columns[0]] + '" ><button onclick="uploadDocOperation(' + sourceData[i][columns[0]] + ')" type="button" class="btn btn-round btn-warning bg-gradient-warning edit" id="edit_' + sourceData[i][columns[0]] + '" style="background-color:#0078d7">Document</button></td>';
                } else if (actionColumnsData[v] == 'view') {
                    data += '<td id="td_view_' + sourceData[i][columns[0]] + '" ><button onclick="viewOperation(' + sourceData[i][columns[0]] + ')" type="button" class="btn btn-round btn-primary edit" data-toggle="modal" data-target="#exampleModal" id="edit_' + sourceData[i][columns[0]] + '" style="background-color:#0078d7">View</button><div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="exampleModalLabel">Modal title</h5><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body"><div class="filetext" id="filetext"></div></div><div class="modal-footer"><button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button></div></div></div></div></td>';
                } else if (actionColumnsData[v] == 'edit') {
                    data += '<td id="td_edit_' + sourceData[i][columns[0]] + '" ><button onclick="editOperation(' + sourceData[i][columns[0]] + ')" type="button" class="btn btn-round btn-primary edit" id="edit_' + sourceData[i][columns[0]] + '" style="background-color:#0078d7">Edit</button></td>';
                } else if (actionColumnsData[v] == 'active') {
                    data += '<td id="td_active_' + sourceData[i][columns[0]] + '" ><button onclick="activeOperation(' + sourceData[i][columns[0]] + ')" type="button" class="btn btn-round btn-primary active" id="active_' + sourceData[i][columns[0]] + '" style="background-color:#0078d7">Active</button></td>';
                } else if (actionColumnsData[v] == 'inactive') {
                    data += '<td id="td_inactive_' + sourceData[i][columns[0]] + '" ><button onclick="inactiveOperation(' + sourceData[i][columns[0]] + ')" type="button" class="btn btn-round btn-danger inactive" id="inactive_' + sourceData[i][columns[0]] + '">InActive</button></td>';
                } else {
                    data += '<td><button id="delete" onclick="deleteOperation(' + sourceData[i][columns[0]] + ')" type="button" class="btn btn-round btn-danger delete">Delete</button></td>';
                }
            }

            data += '</tr>';
        }
    }


    return data;
}


// Other Functions
function getFirst_LastRow(recordNumber, currentPageNumber) {

    //debugger;

    var startRow = parseInt(recordNumber * recordsPerPage);
    var lastRow = parseInt(recordNumber * recordsPerPage) + parseInt(recordsPerPage);
    var bodyStartRow = currentPageNumber != 1 ? startRow : currentPageNumber;
    var bodyLastRow = currentPageNumber != 1 ? lastRow : recordsPerPage;

    if (bodyStartRow == 1 && bodyLastRow == 10) {
        bodyStartRow = 0;
        bodyLastRow = 9;
    } else if (parseInt(bodyStartRow % 10) == 0) {
        bodyLastRow = bodyLastRow - 1
    } else if (bodyStartRow > 10) {
        bodyStartRow = bodyStartRow - 1;
        bodyLastRow = bodyLastRow - 1;
    }

    return [bodyStartRow, bodyLastRow];
}

// OPERATIONS LIKE - EDIT, UPDATE, CANCEL & DELETE *******************************
function activeOperation(id) {
    var filename = $('#td_FileName_' + id).text();
    var tempname = $('.tempnameName_' + id).text();
    $('#active_' + id).attr('disabled', 'true');
    $('#inactive_' + id).prop('disabled', false);
    $.ajax({
        url: 'https://localhost:44360/api/templatedocument',
        type: 'GET',
        crossDomain: true,
        dataType: 'jsonp',
        cors: true,
        contentType: 'application/json',
        secure: true,
        data: {
            templateId: id,
            fileName: filename,
            inUse: false,
            templateName: tempname,
            mode: 7,
        },
        headers: {
            'Access-Control-Allow-Origin': '*',
        },

        success: function(data) {
            print(data);
            //$('#active_' + id).attr('disabled', 'true');
            //$('#inactive_' + id).attr('disabled', 'false');

        }
    });


}

function inactiveOperation(id) {
    var filename = $('#td_FileName_' + id).text();
    var tempname = $('.tempnameName_' + id).text();
    $('#inactive_' + id).attr('disabled', 'true');
    $('#active_' + id).prop('disabled', false);
    $.ajax({
        url: 'https://localhost:44360/api/templatedocument',
        type: 'GET',
        crossDomain: true,
        dataType: 'jsonp',
        cors: true,
        contentType: 'application/json',
        secure: true,
        data: {
            templateId: id,
            fileName: filename,
            inUse: false,
            templateName: tempname,
            mode: 3,
        },
        headers: {
            'Access-Control-Allow-Origin': '*',
        },

        success: function(data) {
            print(data);
            //$('#inactive_' + id).attr('disabled', 'true');

        }
    });
    //$('#active_' + id).attr('disabled', 'false');
    //$('#inactive_' + id).attr('disabled', 'true');

}

function editOperation(id) {
    // Disabling all edit & delete buttons
    $('.edit').attr('disabled', 'true');
    $('.delete').attr('disabled', 'true');
    $('#td_FullName_' + id).css('display', 'none');
    $('#td_Email_' + id).css('display', 'block');
    $('#td_TemplateName_' + id).css('display', 'none');
    $(".tempnameTemplateName_" + id).css('display', 'block');
    $(".tempnameFullName_" + id).css('display', 'block');
    $(".tempnameEmail_" + id).css('display', 'none');
    //$('.tempname' + id).css('display', 'block');
    $('#edit_' + id).hide();

    $('#td_edit_' + id).append('<button onclick="updateOperation(' + id + ')" type="button" class="btn btn-round btn-success bg-gradient-success" id="update_' + id + '" style="background-color:#0078d7">Update</button>');
    $('#td_edit_' + id).append('<button onclick="cancelOperation(' + id + ')" type="button" class="btn btn-round btn-light" id="cancel_' + id + '">Cancel</button>');
    //var x= document.getElementsByClassName('tempname'+id);
    //var x= $('#tempname'+id).val(); 
    //alert(x);


}

function cancelOperation(id) {
    document.getElementById('update_' + id).remove();
    document.getElementById('cancel_' + id).remove();
    $('.tempnameTemplateName_' + id).css('display', 'none');
    $('.tempnameFullName_' + id).css('display', 'none');
    //$('.tempnameEmail_' + id).css('display', 'none');
    $('.tempname' + id).css('display', 'none');
    $('#td_TemplateName_' + id).css('display', 'block');
    $('#td_FullName_' + id).css('display', 'block');
    $('#td_Email_' + id).css('display', 'block');
    $('#edit_' + id).show();

    // Enabling all edit & delete buttons
    $('.edit').prop('disabled', false);
    $('.delete').prop('disabled', false);

}

function deleteOperation(id) {
    var y = $("#td_TemplateName_" + id).text();
    var x = $("#td_FileName_" + id).text();
    var z = $("#td_FullName_" + id).text();
    if (x == x && x != y && x != z && x != "") {
        var filename = $("#td_FileName_" + id).text();
        var tempname = $('.tempnameName_' + id).val();
        console.log(tempname);
        //alert(filename);
        $.ajax({
            url: 'https://localhost:44360/api/templatedocument',
            type: 'GET',
            data: {
                templateId: id,
                fileName: filename,
                inUse: true,
                templateName: tempname,
                mode: 8,
            },
            success: function(data) {
                $('#tr_' + id).remove();
            }
        });
        var x = $('#doccount').text();
        var count = x - 1;
        $('#doccount').text(count);
        $('#tr_' + id).remove();

    } else if (y == y && y != x && y != z && y != "") {

        var tempname = $("#td_TemplateName_" + id).text();
        //var del_id = $(this).attr("id")
        $.ajax({
            url: 'https://localhost:44360/api/template',
            type: 'GET',
            data: {
                templateID: id,
                templateName: tempname,
                mode: 3,

            },
            success: function(data) {
                $('#tr_' + id).remove();
            }
        });
        $('#tr_' + id).remove();
        var x = $('#count1').text();
        var count = x - 1;
        $('#count1').text(count);


    } else {
        var fullname = $("#td_Email_" + id).text();
        // alert(x);
        //var del_id = $(this).attr("id")
        $.ajax({
            url: 'https://localhost:44360/api/adduser',
            type: 'GET',
            data: {
                userID: id,
                userTypeID: 1,
                QRID: "QR-11",
                firstName: "x",
                lastName: "x",
                username: fullname,
                password: "123",
                mode: 3
            },
            success: function(data) {
                $('#tr_' + id).remove();
            }
        });
        $.ajax({
            // points to the url where your data will be posted
            url: "/getusertypeid",
            // post for security reason
            type: "GET",

            // data that you will like to return
            data: { stock: fullname },
            headers: { "X-CSRFToken": "{{ csrf_token }}" },
            processData: true,
            contentType: true,
            // what to do when the call is success
            success: function(response) {
                var x = response;
                if (x == "1") {
                    var x = $('#totaluser').text();
                    var count = x - 1;
                    $('#totaluser').text(count);
                    var y = $('#admin').text();
                    var count1 = y - 1;
                    $('#admin').text(count1);

                } else {
                    var x = $('#users').text();
                    var count = x - 1;
                    $('#users').text(count);
                    var y = $('#totaluser').text();
                    var count1 = y - 1;
                    $('#totaluser').text(count1);
                }
            },
            // what to do when the call is complete ( you can right your clean from code here)
        });
        //var x = $('#count1').text();
        //var count = x - 1;
        //$('#count1').text(count);
        $('#tr_' + id).remove();
    }
}

function updateOperation(id) {

    $(".tempnameFullName_" + id).css('border-color', 'black');
    var y = $(".tempnameFullName_" + id).val();
    console.log("name " + y);
    var z = $(".tempnameEmail_" + id).val();
    var x = $(".tempnameTemplateName_" + id).val();
    console.log(x);
    //var x = $('.tempname' + id).val();
    //alert(x);
    if (x == undefined) {
        if (y == "" || y == undefined || y == null) {
            $(".tempnameFullName_" + id).css("border", "1px solid red");
            return false;

        } else {
            $.ajax({
                url: 'https://localhost:44360/api/adduser',
                type: 'GET',
                data: {
                    userID: id,
                    userTypeID: 1,
                    QRID: "QR-859",
                    firstName: y,
                    lastName: "x",
                    username: z,
                    password: "123",
                    mode: 5
                },
                success: function() {
                    $('.tempnameFullName_' + id).val(y);
                    $('#td_FullName_' + id).text(y);


                }
            });
        }
        $('.tempnameFullName_' + id).val(y);
        //$('.tempnameEmail_' + id).val(z);
        $('#td_FullName_' + id).text(y);
        //$('#td_Email_' + id).text(z);

        $('#edit_' + id).show();
        document.getElementById('update_' + id).remove();
        document.getElementById('cancel_' + id).remove();
        $(".tempnameFullName_" + id).css('display', 'none');
        $('#td_FullName_' + id).css('display', 'block');
        // Enabling all edit & delete buttons
        $('.edit').prop('disabled', false);
        $('.delete').prop('disabled', false);
        // -----------------------------





    } else {
        if (x == "" || x == undefined) {
            $('.tempnameTemplateName_' + id).css('border', '1px solid red');
            return false;

        } else {
            $.ajax({
                url: 'https://localhost:44360/api/template',
                type: 'GET',
                data: {
                    templateID: id,
                    templateName: x,
                    mode: 2
                },
                success: function() {

                    $('.tempnameTemplateName_' + id).val(x);
                    $('#td_TemplateName_' + id).text(x);

                }

            });
        }
        // ---------------------------------------
        $('.tempnameTemplateName_' + id).val(x);
        $('#td_TemplateName_' + id).text(x);
        $('#edit_' + id).show();
        document.getElementById('update_' + id).remove();
        document.getElementById('cancel_' + id).remove();
        $("#td_TemplateName_" + id).css('display', 'block');
        $(".tempnameTemplateName_" + id).css('display', 'none');
        // Enabling all edit & delete buttons
        $('.edit').prop('disabled', false);
        $('.delete').prop('disabled', false);
        console.log("user page");


    }



}

function uploadDocOperation(id) {
    var x = $("#td_TemplateName_" + id).text();
    //sessionStorage.setItem("x", x);
    localStorage.setItem("message", x);
    window.open('docupload', "_self");
    // var x = sessionStorage.getItem("x");
    //console.log(x);█

}

function formOperation(id) {

    var x = $("#td_TemplateName_" + id).text();
    //var x = $('.tempnameTemplateName_' + id).val();
    // var x = $('.tempname' + id).val();
    //alert(x);
    localStorage.setItem("message", x);
    window.open('tempform', "_self");

    //window.open('tempform');
}



function viewOperation(i) {
    // //x = $("#td_FileName_" + i).val();
    x = $("#td_FileName_" + i).text();
    $.ajax({
        // points to the url where your data will be posted
        url: '/fileview',
        // post for security reason
        type: "GET",

        // data that you will like to return
        data: { 'stock': x },
        headers: { "X-CSRFToken": '{{ csrf_token }}' },
        processData: true,
        contentType: true,
        // what to do when the call is success
        success: function(response) {
            $('.filetext').text("");
            var filetext = JSON.stringify(response);
            var file = filetext.replace(/^"(.*)"$/, '$1');
            console.log(file);
            $('.filetext').append(file);
        },
        // what to do when the call is complete ( you can right your clean from code here)
        complete: function() {},
        // what to do when there is an error
        error: function(xhr, textStatus, thrownError) {}
    });
}



// SHOWING NO OF RECORDS *************************************

function showRecords(Rows) {

    //debugger;

    var bodyStartRow = Rows[0],
        bodyLastRow = Rows[1];

    $('#NoOfRecords').empty();
    if ((mainBodyData.length - 1) == -1 && bodyLastRow == -1)

        $("#NoOfRecords").append("Showing " + bodyStartRow + " to " + 0 + " records of " + 0);
    else {
        bodyStartRow = bodyStartRow + 1;
        bodyLastRow = bodyLastRow + 1;

        var sourceLength = searchResultsData.length != 0 ? searchResultsData.length : mainBodyData.length;

        if (bodyLastRow > sourceLength)
            $("#NoOfRecords").append("Showing " + bodyStartRow + " to " + sourceLength + " records of " + (sourceLength));
        else
            $("#NoOfRecords").append("Showing " + bodyStartRow + " to " + bodyLastRow + " records of " + (sourceLength));
    }
}


//  CODE FOR PAGINATION STARTS HERE *******************************

function applyPagination() {

    prepareAndBindPaginationScript();
}

function prepareAndBindPaginationScript() {

    $("#divPageNumber").empty();
    $("#divPageNumber").append('<button class="btn btn-primary" id="btnFirstexcel" onclick="firstButtonexcel();"><span class="glyphicon glyphicon-backward"></span> First</button><button class="btn btn-primary bg-gradient-primary" id="btnPreviousexcel" onclick="previousButtonexcel();"><span class="glyphicon glyphicon-step-backward"></span> Previous</button>');

    noOfButtons = getNoOfButtons();

    for (var i = 1; i <= noOfButtons; i++) {
        if (i == 6)
            break;

        if (i == 1)
            $("#divPageNumber").append('<button class="btn btn-success"  onclick="pageNumberButtonClick(\'' + i + '\');">' + i + '</button>');
        else
            $("#divPageNumber").append('<button class="btn btn-primary" onclick="pageNumberButtonClick(\'' + i + '\');">' + i + '</button>');
    }

    if (noOfButtons == 0) {
        $("#divPageNumber").append('<button class="btn btn-success"  onclick="pageNumberButtonClick(\'1\');">1</button>');
    }

    $("#divPageNumber").append('<button class="btn btn-primary" id="btnNext" onclick="nextButtonexcel();"><span class="glyphicon glyphicon-step-forward"></span>  Next</button><button class="btn btn-primary bg-gradient-primary" id="btnLast" onclick="lastButtonexcel();"><span class="glyphicon glyphicon-forward"></span> Last</button>');

    $("#btnFirstexcel").attr("disabled", true);
    $("#btnPreviousexcel").attr("disabled", true);

    if (noOfButtons == 1 || noOfButtons == 0) {
        $("#btnNext").attr("disabled", true);
        $("#btnLast").attr("disabled", true);
    }

}

function getNoOfButtons() {

    var noOfButtons = "";

    if ($("#txtSearch").val() != "" && $("#txtSearch").val() != undefined) {

        noOfButtons = parseInt((searchResultsData.length) / recordsPerPage);

        var checkCount = parseInt((searchResultsData.length) % recordsPerPage);

        if (checkCount >= 1)
            noOfButtons = parseInt(noOfButtons) + 1;
    } else {
        noOfButtons = parseInt((mainBodyData.length) / recordsPerPage);

        var checkCount1 = parseInt((mainBodyData.length) % recordsPerPage);

        if (checkCount1 >= 1)
            noOfButtons = parseInt(noOfButtons) + 1;
    }

    return noOfButtons;
}



function pageNumberButtonClick(pageNumber) {
    tableBinding(pageNumber);
    applyPaginationForPageButtonClick();
}

function applyPaginationForPageButtonClick() {

    //debugger;

    var noOfButtons = getNoOfButtons();

    if (noOfButtons == 0)
        return;

    $("#divPageNumber").empty();
    $("#divPageNumber").append('<button class="btn btn-primary" id="btnFirstexcel" onclick="firstButtonexcel();"><span class="glyphicon glyphicon-backward"></span> First</button><button class="btn btn-primary" id="btnPreviousexcel" onclick="previousButtonexcel();"><span class="glyphicon glyphicon-step-backward"></span> Previous</button>');

    if (currentPageNumber < 5) {

        for (var i = 1; i <= noOfButtons; i++) {
            if (i == 6)
                break;

            if (i == currentPageNumber)
                $("#divPageNumber").append('<button class="btn btn-success" onclick="pageNumberButtonClick(\'' + i + '\');">' + i + '</button>');
            else
                $("#divPageNumber").append('<button class="btn btn-primary" onclick="pageNumberButtonClick(\'' + i + '\');">' + i + '</button>');
        }
    } else {
        if (currentPageNumber == noOfButtons) {

            $("#divPageNumber").append('<button class="btn btn-primary" onclick="pageNumberButtonClick(\'' + (parseInt(currentPageNumber) - 4) + '\');">' + (parseInt(currentPageNumber) - 4) + '</button>');
            $("#divPageNumber").append('<button class="btn btn-primary" onclick="pageNumberButtonClick(\'' + (parseInt(currentPageNumber) - 3) + '\');">' + (parseInt(currentPageNumber) - 3) + '</button>');
            $("#divPageNumber").append('<button class="btn btn-primary" onclick="pageNumberButtonClick(\'' + (parseInt(currentPageNumber) - 2) + '\');">' + (parseInt(currentPageNumber) - 2) + '</button>');
            $("#divPageNumber").append('<button class="btn btn-primary" onclick="pageNumberButtonClick(\'' + (parseInt(currentPageNumber) - 1) + '\');">' + (parseInt(currentPageNumber) - 1) + '</button>');
            $("#divPageNumber").append('<button class="btn btn-success"  onclick="pageNumberButtonClick(\'' + currentPageNumber + '\');">' + currentPageNumber + '</button>');
        } else if (currentPageNumber <= noOfButtons - 2) {
            $("#divPageNumber").append('<button class="btn btn-primary" onclick="pageNumberButtonClick(\'' + (parseInt(currentPageNumber) - 2) + '\');">' + (parseInt(currentPageNumber) - 2) + '</button>');
            $("#divPageNumber").append('<button class="btn btn-primary" onclick="pageNumberButtonClick(\'' + (parseInt(currentPageNumber) - 1) + '\');">' + (parseInt(currentPageNumber) - 1) + '</button>');
            $("#divPageNumber").append('<button class="btn btn-success" onclick="pageNumberButtonClick(\'' + currentPageNumber + '\');">' + currentPageNumber + '</button>');
            $("#divPageNumber").append('<button class="btn btn-primary" onclick="pageNumberButtonClick(\'' + ((parseInt(currentPageNumber) + 1)) + '\');">' + ((parseInt(currentPageNumber) + 1)) + '</button>');
            $("#divPageNumber").append('<button class="btn btn-primary" onclick="pageNumberButtonClick(\'' + (parseInt(currentPageNumber) + 2) + '\');">' + (parseInt(currentPageNumber) + 2) + '</button>');
        } else if (currentPageNumber <= noOfButtons - 1) {
            $("#divPageNumber").append('<button class="btn btn-primary" onclick="pageNumberButtonClick(\'' + (parseInt(currentPageNumber) - 3) + '\');">' + (parseInt(currentPageNumber) - 3) + '</button>');
            $("#divPageNumber").append('<button class="btn btn-primary" onclick="pageNumberButtonClick(\'' + (parseInt(currentPageNumber) - 2) + '\');">' + (parseInt(currentPageNumber) - 2) + '</button>');
            $("#divPageNumber").append('<button class="btn btn-primary" onclick="pageNumberButtonClick(\'' + (parseInt(currentPageNumber) - 1) + '\');">' + (parseInt(currentPageNumber) - 1) + '</button>');
            $("#divPageNumber").append('<button class="btn btn-success" onclick="pageNumberButtonClick(\'' + currentPageNumber + '\');">' + currentPageNumber + '</button>');
            $("#divPageNumber").append('<button class="btn btn-primary" onclick="pageNumberButtonClick(\'' + ((parseInt(currentPageNumber) + 1)) + '\');">' + ((parseInt(currentPageNumber) + 1)) + '</button>');
        }
    }
    $("#divPageNumber").append('<button class="btn btn-primary" id="btnNext" onclick="nextButtonexcel();"><span class="glyphicon glyphicon-step-forward"></span>  Next</button><button class="btn btn-primary" id="btnLast" onclick="lastButtonexcel();"><span class="glyphicon glyphicon-forward"></span> Last</button>');

    if (currentPageNumber == 1) {
        $("#btnFirstexcel").attr("disabled", true);
        $("#btnPreviousexcel").attr("disabled", true);
    }

    if (currentPageNumber == noOfButtons) {
        $("#btnNext").attr("disabled", true);
        $("#btnLast").attr("disabled", true);
    }
}

function firstButtonexcel() {
    //////debugger;
    tableBinding(1);
    applyPagination();
}

function previousButtonexcel() {
    // var value = $(".btn-success").text().toLocalecaseCase();

    var value = $("#divPageNumber").find('.btn-success').text();

    var m = value.indexOf("submit");

    if (m !== -1)
        value = value.replace(/submit/g, "");

    pageNumberButtonClick(parseInt(value) - parseInt(1));
}


function nextButtonexcel() {
    //////debugger;

    //var value = $(".btn-success").text().toLocaleLowerCase();
    var value = $("#divPageNumber").find('.btn-success').text();

    var m = value.indexOf("submit");

    if (m !== -1)
        value = value.replace(/submit/g, "");

    pageNumberButtonClick(parseInt(value) + parseInt(1));
}

function lastButtonexcel() {
    //////debugger;

    var noOfButtons = "";

    if ($("#txtSearch").val() != "" && $("#txtSearch").val() != undefined) {
        noOfButtons = parseInt((searchResultsData.length) / recordsPerPage);

        var checkCount = parseInt((searchResultsData.length) % recordsPerPage);

        if (checkCount >= 1)
            noOfButtons = parseInt(noOfButtons) + 1;
    } else {
        noOfButtons = parseInt((mainBodyData.length) / recordsPerPage);

        var checkCount = parseInt((mainBodyData.length) % recordsPerPage);

        if (checkCount >= 1)
            noOfButtons = parseInt(noOfButtons) + 1;
    }

    pageNumberButtonClick(noOfButtons);
}


// SEARCH FUNCTIONALITY *****************************************

function searchData() {
    //debugger;
    var input, searchVal = '',
        i;
    input = document.getElementById("txtSearch");
    searchVal = input.value.toLowerCase();

    searchResultsData = [];

    for (i = 0; i < mainBodyData["length"]; i++) {

        if (mainBodyData[i][searchField].toLowerCase().indexOf(searchVal.toString()) !== -1) {
            searchResultsData.push(mainBodyData[i]);
        }
    }

    tableBinding(1);
    applyPagination();
}