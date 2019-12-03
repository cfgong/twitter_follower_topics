const INITIAL_STATE = {
  searched: "",
};

const applySetSearched = (state, action) => ({
  ...state,
  searched: action.payload
});

function searchedReducer(state = INITIAL_STATE, action) {
  switch(action.type) {
    case 'SEARCHED_SET' : {
      return applySetSearched(state, action);
    }
    default : return state;
  }
}

export default searchedReducer;