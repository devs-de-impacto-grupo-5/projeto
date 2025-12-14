import styled from 'styled-components';
import { darkPurple, lightYellow, darkYellow, neutral } from '../../constants/colors';

export const Container = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background-color: ${neutral};
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

export const BackButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: ${darkPurple};
  cursor: pointer;
  padding: 4px;

  &:hover {
    opacity: 0.7;
  }
`;

export const LogoWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
`;

export const HelpButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: ${lightYellow};
  border: none;
  color: ${darkYellow};
  cursor: pointer;

  &:hover {
    opacity: 0.9;
  }
`;
