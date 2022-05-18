import { tokenConfig, tokenConfigForm } from "./ActionAuth";

const URL = "http://127.0.0.1:8000/api/";

function ActionGetAllFlows() {
  let link = URL + "flows/";
  return fetch(link, tokenConfig());
}

function ActionGetFlow(id) {
  let link = URL + `flows/${id}/`;
  return fetch(link, tokenConfig());
}

function ActionCreateFlow(data) {
  let link = URL + "flows/";
  return fetch(link, {
    method: "POST", // or 'PUT'
    headers: tokenConfig().headers,
    body: JSON.stringify(data),
  });
}

function ActionSetData(id, data) {
  const setTestAndTrainDataURL = `${URL}flows/${id}/set_data/`;
  return fetch(setTestAndTrainDataURL, {
    method: "POST",
    headers: tokenConfigForm().headers,
    body: data,
  });
}

function ActionSetDataTest(id, data) {
  const setTestAndTrainDataURL = `${URL}flows/${id}/set_data_test/`;
  return fetch(setTestAndTrainDataURL, {
    method: "POST",
    headers: tokenConfigForm().headers,
    body: data,
  });
}

function ActionAppendData(id, data) {
  const setTestAndTrainDataURL = `${URL}flows/${id}/append_data/`;
  return fetch(setTestAndTrainDataURL, {
    method: "POST",
    headers: tokenConfigForm().headers,
    body: data,
  });
}

function ActionGetGatheringDataInfo(id) {
  let link = `${URL}flows/${id}/get_gathering_data_info/`;
  return fetch(link, tokenConfig());
}

function ActionPrepareData(id, data) {
  const link = `${URL}flows/${id}/prepare_data/`;

  return fetch(link, {
    method: "POST",
    headers: tokenConfig().headers,
    body: JSON.stringify(data),
  });
}

function ActionGetAllModels(id, data) {
  const link = `${URL}flows/${id}/get_all_flow_models/`;

  return fetch(link, tokenConfig());
}

function ActionCreateNewModel(id, data) {
  const link = `${URL}flows/${id}/create_model/`;

  return fetch(link, {
    method: "POST",
    headers: tokenConfig().headers,
    body: JSON.stringify(data),
  });
}


function ActionGetTrainAndTestInfo(id, data) {
  const link = `${URL}flows/${id}/get_train_and_test_info/`;

  return fetch(link, {
    method: "POST",
    headers: tokenConfig().headers,
    body: JSON.stringify(data),
  });
}

function ActionSetModelHyperParameters(id, data) {
  const link = `${URL}flows/${id}/set_model_hyperparameters/`;

  return fetch(link, {
    method: "POST",
    headers: tokenConfig().headers,
    body: JSON.stringify(data),
  });
}


function ActionTrainData(id, data) {
  const link = `${URL}flows/${id}/train_data/`;

  return fetch(link, {
    method: "POST",
    headers: tokenConfig().headers,
    body: JSON.stringify(data),
  });
}

function ActionTestData(id, data) {
  const setTestAndTrainDataURL = `${URL}flows/${id}/test_data/`;
  return fetch(setTestAndTrainDataURL, {
    method: "POST",
    headers: tokenConfigForm().headers,
    body: data,
  });
}

function ActionGetAllFlowModels(id) {
  const url = `${URL}flows/${id}/get_all_flow_models/`;
  return fetch(url, {
    method: "GET",
    headers: tokenConfigForm().headers,
  });
}

export {
  ActionGetAllFlows,
  ActionCreateFlow,
  ActionSetData,
  ActionSetDataTest,
  ActionGetGatheringDataInfo,
  ActionGetFlow,
  ActionAppendData,
  ActionPrepareData,
  ActionGetTrainAndTestInfo,
  ActionTrainData,
  ActionTestData,
  ActionGetAllFlowModels,
  ActionGetAllModels,
  ActionCreateNewModel,
  ActionSetModelHyperParameters,
};
