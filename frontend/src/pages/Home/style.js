import styled from 'styled-components';
import { darkPurple, darkYellow, lightGreen, neutral } from '../../constants/colors';
import { largeSpacing } from '../../constants/spacing';

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
  background-color: ${neutral};
`;

export const LogoWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  width: 100%;
`;

export const LogoImage = styled.img`
  width: 40%;
`

export const Slogan = styled.h2`
  font-size: 1.5rem;
  font-size: 20px;
  width: 80%;
  text-align: center;
  font-weight: 600;
  color: ${darkPurple};
  margin-bottom: ${largeSpacing};
`;

export const ProdutorWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 150px;
  height: 150px;
  background-color: ${lightGreen};
  border-radius: 50%;
  margin-bottom: ${largeSpacing};
`;

export const ProdutorImage = styled.img`
  width: 250px;
  height: auto;
  position: relative;
`;

export const Question = styled.h3`
  font-size: 14px;
  color: ${darkPurple};
  text-align: center;
  width: 80%;
  font-weight: 700;
  margin-bottom: ${largeSpacing};
`;

export const ButtonsWrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  align-items: center;
  margin-bottom: ${largeSpacing};
`;

export const ChangeAccountType = styled.small`
  color: ${darkYellow};
  text-align: center;
  width: 100%;
`;