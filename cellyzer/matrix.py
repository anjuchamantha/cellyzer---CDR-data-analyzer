matrix_css = """
table {
  position: relative;
  width: 1320px;
  background-color: #aaa;
  overflow: hidden;
  border-collapse: collapse;
}


/*thead*/
thead {
  position: relative;
  width: 1320px;
  display: block; /*seperates the header from the body allowing it to be positioned*/
  overflow: visible;
}

thead th {
  background-color: #99a;
  min-width: 120px;
  height: 32px;
  border: 1px solid #222;
}

thead th:nth-child(1) {/*first cell in the header*/
  position: relative;
  display: block; /*seperates the first cell in the header from the header*/
  background-color: #88b;
}


/*tbody*/
tbody {
  position: relative;
  display: block; /*seperates the tbody from the header*/
  height: 500px;
  width: 1320px;
  overflow: scroll;
}

tbody td {
  background-color: #bbc;
  min-width: 120px;
  border: 1px solid #222;
}

tbody tr td:nth-child(1) {  /*the first cell in each tr*/
  position: relative;
  display: block; /*seperates the first column from the tbody*/
  height: 40px;
  background-color: #99a;
}
"""

matrix_js = """
    function scroll() {
      $('tbody').scroll(function(e) { //detect a scroll event on the tbody
        /*
        Setting the thead left value to the negative value of tbody.scrollLeft will make it track the movement
        of the tbody element. Setting an elements left value to that of the tbody.scrollLeft left makes it maintain 			it's relative position at the left of the table.
        */
        $('thead').css("left", -$("tbody").scrollLeft()); //fix the thead relative to the body scrolling
        $('thead th:nth-child(1)').css("left", $("tbody").scrollLeft()); //fix the first cell of the header
        $('tbody td:nth-child(1)').css("left", $("tbody").scrollLeft()); //fix the first column of tdbody
      });
    };
"""

matrix_html_head = """
<html>
    <head>
        <style>
            {}
        </style>
        <script>
            {}
        </script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    </head>
    <body>
        <h1>Connection Matrix</h1>
    
""".format(matrix_css, matrix_js)
