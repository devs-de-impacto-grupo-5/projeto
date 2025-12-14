import styled from 'styled-components';
import { lighnerPurple, darkPurple, darkYellow, lightYellow, neutral } from '../../constants/colors';

export const Container = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(12px);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border-bottom: 1px solid #edf0f3;
  position: sticky;
  top: 0;
  z-index: 10;
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
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: ${lighnerPurple};
  flex-shrink: 0;
`;

export const TextContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
`;

export const Subtitle = styled.p`
  font-size: 12px;
  font-weight: 400;
  margin: 0;
  opacity: 0.7;
`;

export const Title = styled.h2`
  font-size: 16px;
  font-weight: 700;
  color: ${darkPurple};
  margin: 0;
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
