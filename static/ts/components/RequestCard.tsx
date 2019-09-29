import React, { FunctionComponent } from 'react';
import { Card, CardBody, CardHeader, CardFooter, Row, Col } from 'reactstrap';
import { isEmpty } from '../utils';
import Moment from 'react-moment'
import Octicon, { Code, CloudDownload } from '@primer/octicons-react'
import { Request } from "../types";

type RequestHeaderProps = {
    method: string,
    path: string,
    contentType: string,
    contentSize: number,
    host: string
}

type RequestFooterProps = {
    time: string
}

type KeyValueListProps = {
    obj: any
}

const RequestHeader: FunctionComponent<RequestHeaderProps> = ({ method, path, contentType, contentSize, host }) => (
    <CardHeader className="request-header align-items-center">
        <div className="float-left">
            <ul className="list-unstyled request-attributes">
                <li><strong>{ method }</strong> { path }</li>
                <li className="text-muted">from { host }</li>
            </ul>
        </div>
        <div className="float-right">
            <ul className="list-unstyled request-attributes">
                { contentType && <li><Octicon icon={ Code }/>
                    &nbsp;<small>{ contentType }</small>
                </li> }
                <li><Octicon icon={ CloudDownload }/>
                    &nbsp;<small>{ contentSize ? contentSize : 0 } bytes</small>
                </li>
            </ul>
        </div>
    </CardHeader>
);

const RequestFooter: FunctionComponent<RequestFooterProps> = ({ time }) => (
    <CardFooter className="text-center text-muted">
        <Moment date={ time } interval={ 1000 } fromNow/>
    </CardFooter>
);

const KeyValueList: FunctionComponent<KeyValueListProps> = ({ obj }) => (
    <ul className="list-unstyled">
        { Object.entries(obj).map(([k, v]) => {
            return (
                <li key={ k }>
                    <strong>{ k }: </strong> { v }
                </li>
            );
        }) }
    </ul>
);

const Subtitle: FunctionComponent = ({ children }) => <h6 className="text-muted text-uppercase">{ children }</h6>;

const None = () => <p><em>None</em></p>;

const RequestCard: FunctionComponent<Request> = ({ method, path, time, body, queryParams, formParams, headers, host }) => (
    <Card className="mb-2">
        <RequestHeader
            method={ method }
            path={ path }
            contentType={ headers['Content-Type'] }
            contentSize={ headers['Content-Length'] }
            host={ host }
        />
        <CardBody>
            <Row>
                <Col lg>
                    <Subtitle>Query Params</Subtitle>
                    { isEmpty(queryParams) ? <None/> : <KeyValueList obj={ queryParams }/> }
                    <Subtitle>Form Params</Subtitle>
                    { isEmpty(formParams) ? <None/> : <KeyValueList obj={ formParams }/> }
                    <Subtitle>Raw Body</Subtitle>
                    { isEmpty(body) ?
                        <None/> :
                        <p>
                            <samp>{ body }</samp>
                        </p>
                    }
                </Col>
                <Col lg>
                    <Subtitle>Headers</Subtitle>
                    <KeyValueList obj={ headers }/>
                </Col>
            </Row>
        </CardBody>
        <RequestFooter time={ time }/>
    </Card>
);

export default RequestCard;