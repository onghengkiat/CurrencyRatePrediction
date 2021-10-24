import React from 'react';
import BigNumber from './ChartTemplate/BigNumber';
import BigWord from './ChartTemplate/BigWord';
import { CgTime, CgTimelapse } from 'react-icons/cg';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import { FiTrendingDown, FiTrendingUp } from 'react-icons/fi';
import { GoGraph } from 'react-icons/go';


export default function DatasetStatistics({ currency_code, statistics }){
    return (
        <div>
            <Container>
                <Row>
                    <Container id="dashboard-title" fluid>
                        <Row className="justify-content-between">
                            <Col>
                                <GoGraph id="dashboard-title-icon"/>
                                <h5><b>Dataset Statistics</b></h5>
                                <h5 className="text-muted"><b>Currency Code: {currency_code}</b></h5>
                            </Col>
                        </Row>
                    </Container>
                </Row>
            </Container>
            <Row className="justify-content-center" md={2} xs={1}>
                <Col className="chart-container">
                    <BigWord 
                        ChartIcon={ CgTime }
                        ChartIconBackgroundColor={ "#6CDE73" }
                        ChartHeader={ "Date for Minimum Exchange Rate"}
                        ChartBody={ statistics["min_date"] }
                    />
                </Col>
                
                <Col className="chart-container">
                    <BigWord 
                        ChartIcon={ CgTimelapse }
                        ChartIconBackgroundColor={ "#FF7F60" }
                        ChartHeader={ "Date for Maximum Exchange Rate"}
                        ChartBody={ statistics["max_date"] }
                    />
                </Col>
            </Row>
            <Row className="justify-content-center" md={2} xs={1}>
                <Col className="chart-container">
                    <BigNumber 
                        ChartIcon={ FiTrendingDown }
                        ChartIconBackgroundColor={ "#2EAC4D" }
                        ChartIconColor={ "#0C6038" }    
                        ChartHeader={ "Minimum Exchange Rate"}
                        ChartBody={ statistics["min_rate"] }
                    />
                </Col>
                
                <Col className="chart-container">
                    <BigNumber 
                        ChartIcon={ FiTrendingUp }
                        ChartIconBackgroundColor={ "#DB261F" }
                        ChartIconColor={ "#7A081F" }
                        ChartHeader={ "Maximum Exchange Rate"}
                        ChartBody={ statistics["max_rate"] }
                    />
                </Col>
            </Row>
            
        </div>
    );
}