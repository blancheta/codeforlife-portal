    function activateImport(){
        $("#studentNamesFileImport").click();
    }

    var fileReader, theText = document.getElementById("form-create-students").elements.item(1);
    function writeStudents(){
        fileReader = new FileReader();
        fileReader.readAsText(document.getElementById("studentNamesFileImport").files[0]);
        fileReader.addEventListener("loadend", showNames);
    }
    function showNames(){
        names = fileReader.result;
        names = names.split(",").join("\n");
        theText.value+=names;
    }
