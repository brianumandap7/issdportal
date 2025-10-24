	function LaBeLFadeIn(LaBelFiElD){ $("#LaBel"+LaBelFiElD).fadeOut('slow'); }
//===========================================================================================================================================================================
	function MM_openBrWindow(theURL,winName,features){ window.open(theURL,winName,features); }
//===========================================================================================================================================================================
	function isEmptyLte(frmField,fldId,fldName){
		var fld = frmField.value; var ctr=0; var len = fld.length;
		for(var i=0;i<=len;i++){ if (fld.charAt(i)==" ") ctr++; }
		if (len==ctr){ $("#Grp"+fldId).addClass('has-error');  frmField.focus(); return true; }else{ $("#Grp"+fldId).removeClass('has-error'); }//alert(fldName + ' is required.');
		return false;
	}
//===========================================================================================================================================================================
	function isEmpty(frmField,fldId,fldName){
		var fld = frmField.value; var ctr=0; var len = fld.length;
		for(var i=0;i<=len;i++){ if (fld.charAt(i)==" ") ctr++; }
		if (len==ctr){ alert(fldName + ' is required.'); frmField.focus(); return true; }
		return false;
	}
//===========================================================================================================================================================================
	function isEmptyModal(frmField,fldId,fldName){
		var fld = frmField.value; var ctr=0; var len = fld.length;
		for(var i=0;i<=len;i++){ if (fld.charAt(i)==" ") ctr++; }
		if (len==ctr){ 
		        AlertMessages = fldName + ' is required.';
		        ModalAlertEmpty(AlertMessages); frmField.focus(); return true; 
		
		}
		return false;
	}	
//===========================================================================================================================================================================
	 function ChangeColor(tableRow, highLight){ 
		if(highLight){ tableRow.style.backgroundColor = "#89FC97";  /*FDF99F '#ebf5fe'; tableRow.style.backgroundColor = '#ebf5fe'317082;*/ }
	   	else{ tableRow.style.backgroundColor = ''; }
	 }
//===========================================================================================================================================================================
	function ChangePasswordS(){
		show_dialog("#dialog", "<?php echo site_url('UsErMgT/ChangePasswordS'); ?>", "CHANGE PASSWORD");
		set_wh("#dialog", 280, 270);
	}
//===========================================================================================================================================================================
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== ''){
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) { cookieValue = decodeURIComponent(cookie.substring(name.length + 1)); break; }
            }
        }
        return cookieValue;
    }
//===========================================================================================================================================================================