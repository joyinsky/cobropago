import React from 'react';
import ReactDOM from 'react-dom';
import {createStore, applyMiddleware} from 'redux';
import {Provider} from 'react-redux';
import thunk from 'redux-thunk';
import {combinedReducers} from './store';
import {Router, Route, IndexRoute, hashHistory} from 'react-router';
import {syncHistoryWithStore, routerMiddleware} from 'react-router-redux';
import App from './app';
import Login from './components/login';
import {Dashboard} from './components/dashboard';
import UserDetail from './components/userdetail';


// const middleware = routerMiddleware(hashHistory);
const store = createStore(combinedReducers, applyMiddleware(thunk));
const history = syncHistoryWithStore(hashHistory, store);


ReactDOM.render(
  <Provider store={store}>
    <Router history={history}>
      <Route path="/" component={App}>
        <IndexRoute component={Dashboard}/>
        <Route path="user" component={UserDetail}/>
      </Route>
      <Route path="/login" component={Login}/>
    </Router>
  </Provider>,
  document.getElementById('react-app')
);
