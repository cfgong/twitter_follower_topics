const INITIAL_STATE = {
  loading: true,
};

const applySetLoading = (state, action) => ({
  ...state,
  loading: action.payload
});

function loadingReducer(state = INITIAL_STATE, action) {
  switch(action.type) {
    case 'LOADING_SET' : {
      return applySetLoading(state, action);
    }
    default : return state;
  }
}

export default loadingReducer;