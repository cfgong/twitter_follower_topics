const INITIAL_STATE = {
  data: {},
};

const applySetData = (state, action) => ({
  ...state,
  data: action.data
});

function dataReducer(state = INITIAL_STATE, action) {
  switch(action.type) {
    case 'DATA_SET' : {
      return applySetData(state, action);
    }
    default : return state;
  }
}

export default dataReducer;