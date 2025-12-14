import React from 'react';
import { Link } from 'react-router-dom';
import {
    Container,
    Navbar,
    LogoContainer,
    NavLinks,
    MainContent,
    TextSection,
    Headline,
    HighlightLighter,
    CallActionButton,
    ImageSection,
    CircleWrapper,
    PersonImg,
    TopRightBlob,
    BottomLeftBlob
} from './style';

import logo from '../../assets/svgs/horizontal_logo.svg';
import personImage from '../../assets/png/assetPerson.png';
import upperFormat from '../../assets/svgs/upperFormat.svg';
import downFormat from '../../assets/svgs/downFormat.svg';

const Inicio = () => {
    return (
        <Container>
            {/* Background Elements */}
            <TopRightBlob src={upperFormat} alt="" />
            <BottomLeftBlob src={downFormat} alt="" />

            <Navbar>
                <LogoContainer>
                    <Link to="/admin/dash" aria-label="Ir para dashboard do admin" style={{ display: 'inline-block' }}>
                        <img src={logo} alt="Vitalis Logo" />
                    </Link>
                </LogoContainer>
                <NavLinks>
                    <Link to="/admin/dash">Início</Link>
                    {/* Assuming generic routes or # for demo */}
                    <Link to="#">Estatísticas</Link>
                    <Link to="/login">Entrar</Link>
                </NavLinks>
            </Navbar>

            <MainContent>
                <TextSection>
                    <Headline>
                        Vital para quem <HighlightLighter>produz</HighlightLighter>,<br />
                        essencial para quem <HighlightLighter>aprende</HighlightLighter>
                    </Headline>
                    <Link to="/login" style={{ textDecoration: 'none' }}>
                        <CallActionButton>
                            Entrar no Vitalis
                        </CallActionButton>
                    </Link>
                </TextSection>

                <ImageSection>
                    <CircleWrapper>
                        <PersonImg src={personImage} alt="Person with book" />
                    </CircleWrapper>
                </ImageSection>
            </MainContent>
        </Container>
    );
};

export default Inicio;
