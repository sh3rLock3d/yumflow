const URL = 'http://127.0.0.1:8000/api/'

function ActionGetAllFlows() {
    let link = URL + 'flows/'
    let res = fetch(link).then(results => results.json())
    return res
}

function ActionCreateFlow(data) {
    let link = URL + "flows/"
    let res = fetch(link, {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    }).then(response => response.json())
    return res

}

function ActionSetSepetatedTestTrainData(id, data){
    const setTestAndTrainDataURL = `${URL}flows/${id}/set_train_test_data/`
    let res = fetch(setTestAndTrainDataURL, {
        method: 'POST',
        body: data,
    })
        .then(response => response.json())
    
    return res
}

function ActionGetGatheringDataInfo(id){
    let link = `${URL}flows/${id}/get_gathering_data_info/`
    let res = fetch(link)
                .then(results => results.json())
    return res
}

export {ActionGetAllFlows, ActionCreateFlow, ActionSetSepetatedTestTrainData, ActionGetGatheringDataInfo}