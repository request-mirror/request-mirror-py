import * as React from "react";
import RequestCard from './RequestCard'
import { Request } from "../types";
import { FunctionComponent } from "react";

type RequestListProps = {
    requests: Array<Request>
}

const RequestList: FunctionComponent<RequestListProps> = ({ requests }) => (
    <div className="requests">
        { requests.map((request, i) => {
            return (
                <RequestCard
                    key={ i }
                    method={ request.method }
                    path={ request.path }
                    time={ request.time }
                    body={ request.body }
                    queryParams={ request.queryParams }
                    formParams={ request.formParams }
                    headers={ request.headers }
                    host={ request.host }
                />
            );
        }) }
    </div>
);

export default RequestList;
