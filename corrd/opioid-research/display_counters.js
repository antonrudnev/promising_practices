$( document ).ready(function() {
    $.ajax({
        url: "http://localhost:5000/api/v1/counter"
    }).done(function(data) {
        $('#legal_reforms_and_policies').text(JSON.stringify(data['legal_reforms_and_policies'])+' entries');
        $('#medication_assisted_treatment').text(JSON.stringify(data['medication_assisted_treatment'])+' entries');
        $('#overdose_prevention_and_response').text(JSON.stringify(data['overdose_prevention_and_response'])+' entries');
        $('#prevention_and_education').text(JSON.stringify(data['prevention_and_education'])+' entries');
        $('#psychosocial_therapy').text(JSON.stringify(+data['psychosocial_therapy'])+' entries');
        $('#safe_prescribing').text(JSON.stringify(data['safe_prescribing'])+' entries');
        $('#treatment_delivery_models').text(JSON.stringify(data['treatment_delivery_models'])+' entries');
    });
});

