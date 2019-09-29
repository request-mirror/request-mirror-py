interface IDictionary {
    [index: string]: any;
}

export type Request = {
    method: string,
    path: string,
    time: string,
    body: string,
    queryParams: IDictionary,
    formParams: IDictionary,
    headers: IDictionary,
    host: string
}