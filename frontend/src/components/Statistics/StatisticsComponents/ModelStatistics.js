import React from 'react';
import Image from 'react-bootstrap/Image'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import { SiProbot } from 'react-icons/si';

import BigNumber from './ChartTemplate/BigNumber';
import { ImStatsDots, ImStatsBars } from 'react-icons/im';
import { FaSquareRootAlt } from 'react-icons/fa';

export default function ModelStatistics({ pic, modelPerformance }){
    return (
        <div>
            <Row>
                <Container id="dashboard-title" fluid>
                    <Row className="justify-content-between">
                        <Col>
                            <SiProbot id="dashboard-title-icon"/>
                            <h5><b>Predictive Model Performance</b></h5>
                            <h5 className="text-muted"><b>Algorithm: Long Short Term Memory (LSTM)</b></h5>
                        </Col>
                    </Row>
                </Container>
            </Row>

            <Row className="justify-content-center" lg={3} md={2} xs={1}>
                <Col className="chart-container">
                    <BigNumber 
                        ChartIcon={ ImStatsBars }
                        ChartIconBackgroundColor={ "#00203FFF" }
                        ChartIconColor={ "#ADEFD1FF" }    
                        ChartHeader={ "R Square" }
                        ChartBody={ modelPerformance["R2"] }
                    />
                </Col>
                
                <Col className="chart-container">
                    <BigNumber 
                        ChartIcon={ FaSquareRootAlt }
                        ChartIconBackgroundColor={ "#0063B2FF" }
                        ChartIconColor={ "#9CC3D5FF" }
                        ChartHeader={ "RMSE" }
                        ChartBody={ modelPerformance["RMSE"] }
                    />
                </Col>


                <Col className="chart-container">
                    <BigNumber 
                        ChartIcon={ ImStatsDots }
                        ChartIconBackgroundColor={ "#A07855FF" }
                        ChartIconColor={ "#D4B996FF" }
                        ChartHeader={ "MAE" }
                        ChartBody={ modelPerformance["MAE"] }
                    />
                </Col>
            </Row>
            <Image alt='actual_vs_predicted' src={ pic } className="responsive"/>
        </div>
    );
}