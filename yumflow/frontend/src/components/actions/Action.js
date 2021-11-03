import { tokenConfig, tokenConfigForm } from "./ActionAuth"

const URL = 'http://127.0.0.1:8000/api/'

function ActionGetAllFlows() {
    let link = URL + 'flows/'
    let res = fetch(link, tokenConfig()).then(results => results.json())
    return res
}

function ActionGetFlow(id) {
    let link = URL + `flows/${id}/`
    let res = fetch(link, tokenConfig()).then(results => results.json())
    return res
}

function ActionCreateFlow(data) {
    let link = URL + "flows/"
    let res = fetch(link, {
        method: 'POST', // or 'PUT'
        headers: tokenConfig().headers,
        body: JSON.stringify(data),
    }).then(response => response.json())
    return res

}

function ActionSetData(id, data){
    const setTestAndTrainDataURL = `${URL}flows/${id}/set_data/`
    let res = fetch(setTestAndTrainDataURL, {
        method: 'POST',
        headers: tokenConfigForm().headers,
        body: data,
    })
        .then(response => response.json())
    
    return res
}

function ActionAppendData(id, data){
    const setTestAndTrainDataURL = `${URL}flows/${id}/append_data/`
    let res = fetch(setTestAndTrainDataURL, {
        method: 'POST',
        headers: tokenConfigForm().headers,
        body: data,
    })
        .then(response => response.json())
    
    return res
}


function ActionGetGatheringDataInfo(id){
    let link = `${URL}flows/${id}/get_gathering_data_info/`
    let res = fetch(link, tokenConfig())
                .then(results => results.json())
    return res
}

function ActionPrepareData(id, data){
    const link = `${URL}flows/${id}/prepare_data/`
    
    let res = fetch(link, {
        method: 'POST',
        headers: tokenConfig().headers,
        body: JSON.stringify(data),
    })
        .then(response => response.json())
    
    return res
}

function ActionTrainData(id, data){
    const link = `${URL}flows/${id}/train_data/`
    
    let res = fetch(link, {
        method: 'POST',
        headers: tokenConfig().headers,
        body: JSON.stringify(data),
    })
        .then(response => response.json())
    
    return res
}

function ActionTestData(id, data){
    const setTestAndTrainDataURL = `${URL}flows/${id}/test_data/`
    let res = fetch(setTestAndTrainDataURL, {
        method: 'POST',
        headers: tokenConfigForm().headers,
        body: data,
    })
        .then(response => response.json())
    
    return res
}

export {ActionGetAllFlows, ActionCreateFlow, ActionSetData, ActionGetGatheringDataInfo, ActionGetFlow, ActionAppendData, ActionPrepareData, ActionTrainData, ActionTestData}