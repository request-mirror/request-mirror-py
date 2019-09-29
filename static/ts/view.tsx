import '../stylesheets/view'
import IO from 'socket.io-client'
import RequestList from './components/RequestList'
import React, { Component } from 'react'
import * as ReactDOM from 'react-dom'
import { Request } from "./types";

declare var url_root: string;
declare var code: string;

const socket = IO(url_root);

type RequestsState = {
    requests: Array<Request>
}

class Requests extends Component<{}, RequestsState> {

    constructor(props: {}) {
        super(props);
        this.state = { requests: [] };
    }

    _receiveRequest(request: Request) {
        console.log(request);
        const { requests } = this.state;
        requests.unshift(request);
        this.setState({ requests });
    }

    componentDidMount() {
        socket.on('connect', () => socket.emit('join', code));
        socket.on('request', (request: Request) => this._receiveRequest(request));
        socket.on('disconnect', () => socket.emit('leave', code));
    }

    render() {
        return <RequestList requests={ this.state.requests }/>
    }
}

ReactDOM.render(
    <Requests/>,
    document.getElementById('request-list')
);