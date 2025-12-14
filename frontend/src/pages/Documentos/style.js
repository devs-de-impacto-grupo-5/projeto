import styled from 'styled-components';
import { neutral } from '../../constants/colors';

export const PageContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: ${neutral};

  @media (min-width: 768px) {
    height: auto;
    min-height: 100vh;
  }
`;

export const Container = styled.div`
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;

  @media (min-width: 768px) {
    width: 60%;
    margin: 0 auto;
    overflow-y: visible;
  }
`;

export const Title = styled.h1`
  font-size: 20px;
  font-weight: 700;
  margin: 0;
  text-align: center;
`;

export const Description = styled.p`
  font-size: 14px;
  font-weight: 400;
  margin: 0 0 16px 0;
  text-align: center;
  line-height: 1.5;
`;
