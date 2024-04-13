// 查
export interface getTradeMarkReqType {
    pageNo: number,
    pageSize: number
}

// 增
export interface addTradeMarkReqType {
    name: string,
    logo: any
}

// 改
export interface updateTradeMarkReqType {
    index: number,
    name: string,
    logo: string
}

// 删
export interface deleteTradeMarkReqType {
    index: number
}